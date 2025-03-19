---
title: How I Built This Website
artist: tony etienne
hero: https://cdnb.artstation.com/p/assets/images/images/023/659/429/4k/tony-etienne-more-brains-in-jars-001.jpg?1579916139
artist-page: https://www.artstation.com/plongitudes
date: 2025-03-06
visible: true
tags:
  - swe
---
# Let's Talk About FastHTML

[FastHTML](https://fastht.ml/) is probably one of the most exciting things happening in the web world right now. If you haven't seen it before, it's powered by what are called "fast tags"; implementations of every HTML tag as Python functions. Since you can pass python strings as arguments into fast tags, you can quickly hack together a templating system for whatever website you're building. The system becomes very powerful when paired with a web server that can leverage fast tags in responding to HTTP requests. It becomes extraordinarily powerful when paired with a JavaScript library like [htmx](https://htmx.org), allowing you to build fully interactive applications just from your server rendered HTML.

Let's take a look at a simple example first

```python
from fasthtml.common import *

app, router = fast_app()

# When the server gets a HTTP GET
# request, execute the function Index
# Return the output of that function
# as the body of the server's response
@app.get('/')
def Index():
	return Div("Hello, world!")

serve()
```

When we run this program, it will spin up a web server on `localhost:5001`

```bash
curl localhost:5001
```

```html
<!doctype html>
<html>
<head>
    <title>FastHTML page</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css">
    <style>
        :root {
            --pico-font-size: 100%;
        }
    </style>
</head>
<body>
    <div>Hello, world</div>
</body>
</html>
```

Great! Our `body` tag looks right, we have our hello world. One thing to note is that FastHTML includes a bunch of stuff in the header that we don't necessarily want when making a custom website. By default, it includes:

- `htmx` for making interactive server side rendered apps
- `pico.css` for nice default styling
- `surreal.js` for conveniences when writing other javascript
- `fasthtml.js` for other defaults

If we want to make a custom website from scratch, we can disable these defaults.

```python
# ...
app, router = fast_app(default_hdrs=False)
# ...
```

```bash
curl localhost:5001
```

```html
 <!doctype html>
 <html>
   <head>
     <title>FastHTML page</title>
   </head>
   <body>
     <div>Hello, world</div>
   </body>
 </html>
```

Beautiful! A blank canvas.

Now, we can start building custom templates that take arguments.

```python
def TitleSection(title: str, subtitle: str):
    return Div(
        H1(title),
        H2(subtitle)
    )

@app.get('/')
def Index():
    return TitleSection(
        title="In the Beginning...",
        subtitle="A history of beginnings"
    )
```

```html
 <!doctype html>
 <html>
   <head>
     <title>FastHTML page</title>
   </head>
   <body>
     <div>
       <h1>In the Beginning...</h1>
       <h2>A history of beginnings</h2>
     </div>
   </body>
 </html>
```

One of the great features of FastHTML is that you can access any of the HTML tag attributes that you normally would by leveraging Python keyword arguments. This means that we can create custom classes and modify the `class` of our HTML elements. Anything passed into a fast tag as a keyword argument will be rendered as an attribute on the HTML element.

Let's add some CSS to our HTML header, and style our elements.

```python
app, router = fast_app(
    default_hdrs=False,
    hdrs=(
        Style('''
            .title {
              font-size: 24px;
              font-weight: bold;
            }
            .subtitle {
              font-size: 18px;
              color: #666;
            }
        '''),
    )
)

def TitleSection(title: str, subtitle: str):
    return Div(
        H1(title, cls="title"),
        H2(subtitle, cls="subtitle", data_custom="random custom attribute")
    )

@app.get('/')
def Index():
    return TitleSection(
        title="In the Beginning...",
        subtitle="A history of beginnings"
    )
```

```html
<!doctype html>
<html>
<head>
    <title>FastHTML page</title>
    <style>
        .title {
            font-size: 24px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 18px;
            color: #666;
        }
    </style>
</head>
<body>
    <div>
        <h1 class="title">In the Beginning...</h1>
        <h2 data-custom="random custom attribute" class="subtitle">A history of beginnings</h2>
    </div>
</body>
</html>
```

Notice the `data-custom` attribute on our `h2` element!

FastHTML is simple, but ridiculously flexible. It's an engine that produces HTML in response to HTTP requests, and it does it really really well. If you've been doing web development for a while, FastHTML is a breath of fresh air. Makes you wonder why we've been building web applications any other way.

# Styling with Tailwind

Okay, generating HTML is useful, but modern web apps aren't just HTML. Styling all of our elements with