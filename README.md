# Zasper tutorials

Notebooks for learning [Zasper](https://zasper.io) and for demoing it.

- `live-talk/`: short notebooks for a live demo, one feature each.
- `tutorials/`: self-paced lessons with explanations and exercises.
- `examples/nyc_taxi.ipynb`: every New York yellow taxi trip in January 2024, queried with SQL cells.
  Its database is built, not stored: see [Data](#data).
- `examples/deno-data-science.ipynb`: data science in TypeScript on the Deno kernel, with Polars and
  Observable Plot.
- `data/penguins.csv`: the [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) dataset
  (CC0), used in all three languages.

The notebooks are saved without outputs: running them is the point.

## Setup

**Python** (every notebook except the Julia and R ones), with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
uv run python -m ipykernel install --user --name zasper-tutorials --display-name "Python (zasper-tutorials)"
```

This environment also includes the `basedpyright` language server, which Zasper finds in `.venv`
and uses for completion, hover and diagnostics in `tutorials/08-code-intelligence.ipynb`.

**Julia**: install Julia, then run `using Pkg; Pkg.add("IJulia")`. Only the standard library is used.

**R**: install R, then run `install.packages(c("IRkernel", "dplyr", "ggplot2"))` and
`IRkernel::installspec(name = "zasper-tutorials-r", displayname = "R (zasper-tutorials)")`.

Then open this folder in Zasper: `zasper --cwd path/to/zasper-tutorials`.

If a notebook asks for a kernel you do not have, pick another from the kernel picker.

## Live talk

About 20 minutes. Run each notebook top to bottom with **Shift+Enter**.

| Notebook | Show | Say |
|---|---|---|
| `01-hello-zasper` | Markdown and LaTeX, a pandas table, a Plotly chart to hover and zoom, Matplotlib | One binary, real Jupyter kernels, and your `.ipynb` files unchanged. |
| `02-rich-outputs` | HTML, Markdown, LaTeX, SVG, JSON, a 3D surface to rotate, stderr, a traceback | Everything a notebook can show. |
| `03-widgets` | Drag the slider and read it back; the linked pair; the explorer dropdowns; the button | Widgets are live objects in the kernel. Close and reopen the tab: they come back. |
| `04-live-output` | Progress bar, countdown, animation, the 50,000-line firehose | Output streams as it happens, and nothing is dropped. Then run *Stop me* and interrupt it, and answer the *input* prompt. |
| `05-julia` | `@time` on 100 million iterations, `λ`, a type that draws itself as SVG | Any Jupyter kernel. |
| `06-r` | dplyr summary, ggplot2, a model summary | And R, with the tidyverse. |

Cells tagged `demo-only` wait for you: an endless loop to interrupt, and an `input()` prompt.

## Tutorials

| Notebook | Covers |
|---|---|
| `01-notebook-basics` | Cells, edit and command modes, shortcuts, the command palette, kernel state, table of contents, find and replace, export |
| `02-markdown-and-math` | Markdown syntax, tables, code blocks, LaTeX inline and display maths |
| `03-rich-outputs` | MIME bundles, `IPython.display`, images, SVG, JSON, `_repr_html_` on your own classes |
| `04-data-analysis` | A full pandas analysis: load, inspect, clean, summarise, plot and a small classifier |
| `05-interactive-plots` | Plotly Express: scatter, distributions, facets, 3D, animation, maps, graph objects |
| `06-widgets` | ipywidgets: properties, `observe`, `jslink`, `interact`, and a small app |
| `07-kernels-and-execution` | Execution order, streaming output, `clear_output`, interrupting, input, restarting |
| `08-code-intelligence` | Completion from the kernel and the language server, hover, diagnostics, formatting |
| `09-julia` | Julia basics, multiple dispatch, speed, custom rich display |
| `10-r` | R vectors, data frames, dplyr, ggplot2, linear models, IRdisplay |

## Data

`data/penguins.csv` is from the [palmerpenguins](https://github.com/allisonhorst/palmerpenguins)
package by Allison Horst, Alison Hill and Kristen Gorman, released under
[CC0](https://creativecommons.org/publicdomain/zero/1.0/).

`examples/nyc_taxi.db` is built from the [TLC Trip Record
Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) published by New York City's Taxi and
Limousine Commission. It is about 475 MB, so it is not in the repository. Build it once:

```sh
uv run examples/build_nyc_taxi_db.py
```
