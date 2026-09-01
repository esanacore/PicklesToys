// Layout and contrast assertions, evaluated in the page by tests/test_layout.sh.
// Returns a JSON string; the shell side parses verdicts out of it.
//
// This closes GAP-001 and GAP-002 in docs/TEST_PLAN.md. Before it existed, the
// contrast figures in docs/BRAND.md were measured by hand and nothing
// recomputed them, so changing a token *value* to something failing would have
// shipped silently. T-076 only ever guarded which token .overline referenced.
//
// Deliberately does NOT take a hand-written list of selectors to check. A list
// only covers the elements someone remembered to add, which is exactly the
// failure mode this is meant to prevent — a new element with bad contrast is
// invisible to it. This walks every text node on the page instead.
(function () {
  var result = {
    textNodesChecked: 0,
    lowContrast: [],      // text below its WCAG AA floor
    pageOverflowX: false, // horizontal scrollbar = layout burst its container
    outOfViewport: [],    // elements extending past the viewport's right edge
    unreadableSize: []    // body copy shrunk below a legible size
  };

  // --- Colour parsing ---------------------------------------------------
  // Chrome reports colours in two unit systems: rgb()/rgba() uses 0-255
  // channels, while color(srgb r g b / a) uses 0-1 floats. Reading srgb
  // floats as 0-255 makes white look black, which turns a passing element
  // into a reported failure — parse the form, do not assume one.
  function parseColor(str) {
    if (!str || str === "transparent") return null;
    var nums = (str.match(/[\d.]+/g) || []).map(Number);
    if (nums.length < 3) return null;
    var scale = /^color\(/i.test(str) ? 255 : 1;
    return {
      r: nums[0] * scale,
      g: nums[1] * scale,
      b: nums[2] * scale,
      a: nums.length > 3 ? nums[3] : 1
    };
  }

  function luminance(c) {
    var ch = [c.r, c.g, c.b].map(function (v) {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
  }

  function over(fg, bg) {
    // Composite a translucent colour onto an opaque one.
    if (fg.a >= 1) return fg;
    return {
      r: fg.r * fg.a + bg.r * (1 - fg.a),
      g: fg.g * fg.a + bg.g * (1 - fg.a),
      b: fg.b * fg.a + bg.b * (1 - fg.a),
      a: 1
    };
  }

  function ratio(fg, bg) {
    var a = luminance(fg), b = luminance(bg);
    return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  }

  // The colour actually painted behind an element: walk up until an opaque
  // colour is found, compositing translucent layers onto it as we go.
  function effectiveBackground(el) {
    var stack = [];
    for (var node = el; node; node = node.parentElement) {
      var parsed = parseColor(getComputedStyle(node).backgroundColor);
      if (parsed && parsed.a > 0) {
        stack.push(parsed);
        if (parsed.a >= 1) break;
      }
    }
    if (!stack.length) return { r: 255, g: 255, b: 255, a: 1 };
    var base = stack[stack.length - 1];
    for (var i = stack.length - 2; i >= 0; i--) base = over(stack[i], base);
    return base;
  }

  // WCAG 2.1: large text (>=24px, or >=18.66px when bold) needs 3:1; every
  // other run of text needs 4.5:1.
  function floorFor(style) {
    var size = parseFloat(style.fontSize);
    var weight = parseInt(style.fontWeight, 10) || 400;
    var large = size >= 24 || (size >= 18.66 && weight >= 700);
    return large ? 3.0 : 4.5;
  }

  function describe(el) {
    var name = el.tagName.toLowerCase();
    if (el.id) return name + "#" + el.id;
    var cls = (el.getAttribute("class") || "").trim().split(/\s+/)[0];
    return cls ? name + "." + cls : name;
  }

  function hidden(el) {
    var s = getComputedStyle(el);
    if (s.visibility === "hidden" || s.display === "none") return true;
    // Elements mid-reveal read as invisible; the shell forces .is-visible
    // before measuring, so anything still transparent here is genuinely so.
    if (parseFloat(s.opacity) === 0) return true;
    var r = el.getBoundingClientRect();
    return r.width === 0 || r.height === 0;
  }

  // --- Contrast over every text node ------------------------------------
  var seen = {};
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: function (node) {
      return node.nodeValue.trim()
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_REJECT;
    }
  });

  var node;
  while ((node = walker.nextNode())) {
    var el = node.parentElement;
    if (!el || el.closest("script, style, title")) continue;
    if (hidden(el)) continue;

    result.textNodesChecked += 1;

    var style = getComputedStyle(el);
    var fg = parseColor(style.color);
    if (!fg) continue;
    var bg = effectiveBackground(el);
    var solidFg = over(fg, bg);
    var r = ratio(solidFg, bg);
    var floor = floorFor(style);

    if (r < floor) {
      var key = describe(el) + "@" + r.toFixed(2);
      if (!seen[key]) {
        seen[key] = true;
        result.lowContrast.push(
          describe(el) + " " + r.toFixed(2) + ":1 (needs " + floor + ")"
        );
      }
    }

    // Body copy below ~12px is a legibility problem regardless of contrast.
    // The overlines are 12.8px small-caps by design, so the floor is 12.
    var px = parseFloat(style.fontSize);
    if (px < 12) {
      var skey = "size:" + describe(el);
      if (!seen[skey]) {
        seen[skey] = true;
        result.unreadableSize.push(describe(el) + " @" + px + "px");
      }
    }
  }

  // --- Geometry ---------------------------------------------------------
  result.pageOverflowX =
    document.documentElement.scrollWidth > document.documentElement.clientWidth + 1;

  // Anything whose box runs past the right edge is either a layout burst or
  // a deliberate bleed. The blobs bleed on purpose and are aria-hidden
  // decoration, so they are exempt; real content is not.
  var slack = 2;
  document.querySelectorAll(
    "header, main, footer, section, h1, h2, h3, p, ul, li, .card, .tbd, .pill, .swatch, .theme-toggle"
  ).forEach(function (el) {
    if (hidden(el)) return;
    if (el.closest("[aria-hidden='true']")) return;
    var r = el.getBoundingClientRect();
    if (r.right > document.documentElement.clientWidth + slack || r.left < -slack) {
      var key = "vp:" + describe(el);
      if (!seen[key]) {
        seen[key] = true;
        result.outOfViewport.push(
          describe(el) + " [" + Math.round(r.left) + ".." + Math.round(r.right) + "]"
        );
      }
    }
  });

  return JSON.stringify(result);
})();
