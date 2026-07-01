/*
 * 原鑑 Materia — 極簡 Claude-Design 相容 runtime
 * 取代 Claude Design 預覽用的 support.js，讓設計檔的 <sc-if>/<sc-for>/{{ }} 模板
 * 能在任何瀏覽器獨立執行，無外部依賴。
 *
 * 支援：
 *   - class extends DCLogic + this.setState() 觸發重繪
 *   - <sc-if value="{{ expr }}">…</sc-if>
 *   - <sc-for list="{{ arr }}" as="x">…</sc-for>（含巢狀、作用域鏈）
 *   - {{ path }} 於文字與屬性內插（點路徑，如 c.badge.tint）
 *   - onClick="{{ handler }}" 綁定函式（設計檔大小寫在 template 內會被解析為 onclick）
 *   - style-hover="…" 滑鼠移入套用、移出還原
 *   - hint-placeholder-* 設計期提示屬性一律忽略
 */
(function (global) {
  class DCLogic {
    setState(patch) {
      Object.assign(this.state, patch);
      if (this._render) this._render();
    }
  }

  function stripBraces(s) {
    if (!s) return '';
    const m = s.match(/^\{\{\s*([\s\S]+?)\s*\}\}$/);
    return m ? m[1] : s;
  }

  function resolve(expr, scope) {
    expr = expr.trim();
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
    let cur = scope;
    for (const part of expr.split('.')) {
      if (cur == null) return undefined;
      cur = cur[part.trim()];
    }
    return cur;
  }

  function interp(str, scope) {
    return str.replace(/\{\{\s*([^}]+?)\s*\}\}/g, function (_, e) {
      const v = resolve(e, scope);
      return v == null ? '' : String(v);
    });
  }

  function applyHover(el, hoverCss, on) {
    if (on) {
      if (el.__baseStyle == null) el.__baseStyle = el.getAttribute('style') || '';
      el.setAttribute('style', el.__baseStyle + ';' + hoverCss);
    } else if (el.__baseStyle != null) {
      el.setAttribute('style', el.__baseStyle);
    }
  }

  function processNode(node, scope, out) {
    if (node.nodeType === Node.TEXT_NODE) {
      out.appendChild(document.createTextNode(interp(node.nodeValue, scope)));
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    const tag = node.tagName.toLowerCase();

    if (tag === 'sc-if') {
      if (resolve(stripBraces(node.getAttribute('value')), scope)) {
        node.childNodes.forEach((ch) => processNode(ch, scope, out));
      }
      return;
    }

    if (tag === 'sc-for') {
      const list = resolve(stripBraces(node.getAttribute('list')), scope) || [];
      const as = node.getAttribute('as') || 'item';
      Array.prototype.forEach.call(list, function (item, idx) {
        const s2 = Object.create(scope);
        s2[as] = item;
        s2[as + '_index'] = idx;
        node.childNodes.forEach((ch) => processNode(ch, s2, out));
      });
      return;
    }

    const el = document.createElement(node.tagName);
    for (const attr of Array.from(node.attributes)) {
      const name = attr.name;
      if (name.startsWith('hint-placeholder')) continue;
      if (name === 'onclick') {
        const fn = resolve(stripBraces(attr.value), scope);
        if (typeof fn === 'function') {
          el.addEventListener('click', function (ev) {
            ev.preventDefault();
            fn(ev);
          });
        }
        continue;
      }
      if (name === 'style-hover') {
        const hover = attr.value;
        el.addEventListener('mouseenter', () => applyHover(el, hover, true));
        el.addEventListener('mouseleave', () => applyHover(el, hover, false));
        continue;
      }
      el.setAttribute(name, interp(attr.value, scope));
    }
    node.childNodes.forEach((ch) => processNode(ch, scope, el));
    out.appendChild(el);
  }

  function renderTemplate(html, scope) {
    const tpl = document.createElement('template');
    tpl.innerHTML = html;
    const frag = document.createDocumentFragment();
    tpl.content.childNodes.forEach((ch) => processNode(ch, scope, frag));
    return frag;
  }

  global.DCLogic = DCLogic;
  global.DCMount = function (ComponentClass, templateHTML, rootEl) {
    const inst = new ComponentClass();
    inst._render = function () {
      const vals = inst.renderVals();
      rootEl.textContent = '';
      rootEl.appendChild(renderTemplate(templateHTML, vals));
    };
    inst._render();
    return inst;
  };
})(window);
