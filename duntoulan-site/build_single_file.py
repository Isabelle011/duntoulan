# -*- coding: utf-8 -*-
"""把 8 个页面 + CSS + 全部图片合并成一个单文件 HTML（图片内嵌为 base64）。"""
import base64, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "images")

PAGES = [
    ("home", "index.html", "首页", "墩头蓝 · 河源客家蓝染非遗"),
    ("culture", "culture.html", "墩头蓝文化", "墩头蓝文化 · 墩头蓝"),
    ("process", "process.html", "工艺流程", "传统工艺流程 · 墩头蓝"),
    ("works", "works.html", "作品展示", "作品展示 · 墩头蓝"),
    ("shop", "shop.html", "文创产品", "文创产品 · 墩头蓝"),
    ("courses", "courses.html", "体验课程", "体验课程 · 墩头蓝"),
    ("news", "news.html", "新闻资讯", "新闻资讯 · 墩头蓝"),
    ("contact", "contact.html", "联系我们", "联系我们 · 墩头蓝"),
]

_cache = {}
def data_uri(rel):
    """images/xxx.jpg -> data:image/jpeg;base64,..."""
    name = os.path.basename(rel)
    if name in _cache:
        return _cache[name]
    path = os.path.join(IMG, name)
    ext = os.path.splitext(name)[1].lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        uri = "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())
    _cache[name] = uri
    return uri

# ── 1. 样式：内联，并把图片路径换成内嵌数据 ──
css = open(os.path.join(ROOT, "css", "style.css"), encoding="utf-8").read()
css = re.sub(r"url\('\.\./images/([^']+)'\)", lambda m: "url('%s')" % data_uri(m.group(1)), css)
css += """
/* ── 单文件版的页面切换 ── */
.page{display:none}
.page.on{display:block}
"""

# ── 2. 逐页抽取正文（去掉各自的 header / footer） ──
page_html = []
for pid, fname, label, title in PAGES:
    html = open(os.path.join(ROOT, fname), encoding="utf-8").read()
    body = html.split("</header>", 1)[1]
    body = body.split("<footer>", 1)[0]
    # 图片内嵌
    body = re.sub(r'src="images/([^"]+)"', lambda m: 'src="%s"' % data_uri(m.group(1)), body)
    # 页面间链接改为哈希路由
    def repl(m):
        target = m.group(1).replace(".html", "")
        return 'href="#%s"' % ("home" if target == "index" else target)
    body = re.sub(r'href="([a-z]+)\.html"', repl, body)
    page_html.append('<div class="page" id="p-%s" data-title="%s">\n%s\n</div>' % (pid, title, body))
    print("打包", fname, "->", pid)

# ── 3. 导航 ──
nav = "\n".join('      <a href="#%s" data-page="%s">%s</a>' % (p[0], p[0], p[2]) for p in PAGES)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>墩头蓝 · 河源客家蓝染非遗</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
%s
</style>
</head>
<body>

<!-- 单文件版：8 个页面全部内嵌在本文件中，靠顶部导航切换，无需其他文件 -->
<header>
  <div class="wrap nav">
    <div class="logo">
      <img class="logo-mark" src="%s" alt="河源墩头蓝徽标">
      <span class="logo-name">墩头蓝</span>
    </div>
    <nav class="menu">
%s
    </nav>
  </div>
</header>

%s

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>墩头蓝</h4>
        <p>致力于墩头蓝纺织印染技艺的传承、传播与创新，让百年蓝染走进当代生活。</p>
      </div>
      <div>
        <h4>联系方式</h4>
        <p>电话：0762-XXXX XXXX</p>
        <p>邮箱：info@duntoulan.com</p>
        <p>工作时间：09:00 - 18:00</p>
      </div>
      <div>
        <h4>地址</h4>
        <p>广东省河源市和平县<br>彭寨镇墩头村</p>
      </div>
      <div>
        <h4>友情链接</h4>
        <a href="#">中国非物质文化遗产网</a>
        <a href="#">广东省非遗保护中心</a>
        <a href="#">河源市文化馆</a>
        <a href="#">和平县融媒体中心</a>
      </div>
    </div>
    <div class="foot-bottom">© 2026 墩头蓝非遗文化中心 · 保留所有权利</div>
  </div>
</footer>

<script>
var PAGE_IDS = ["%s"];
function showPage(id){
  if (PAGE_IDS.indexOf(id) < 0) id = "home";
  document.querySelectorAll(".page").forEach(function(p){
    p.classList.toggle("on", p.id === "p-" + id);
  });
  document.querySelectorAll(".menu a").forEach(function(a){
    a.classList.toggle("active", a.dataset.page === id);
  });
  var el = document.getElementById("p-" + id);
  if (el) document.title = el.dataset.title || document.title;
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", function(){ showPage(location.hash.slice(1)); });
showPage(location.hash.slice(1) || "home");
</script>

</body>
</html>
""" % (css, data_uri("logo.png"), nav, "\n\n".join(page_html), '","'.join(p[0] for p in PAGES))

out = os.path.join(os.path.dirname(ROOT), "墩头蓝网站-单文件版.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("完成:", out, "%.1f MB" % (os.path.getsize(out) / 1024 / 1024))
