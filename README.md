# crystalSearch

An MVC-patterned Python application which works on vectorized image data written to [DataStax Astra DB](https://astra.datastax.com). The application uses the [Flask](https://https://flask.palletsprojects.com/en/3.0.x/) library to build a small front end to allow for dropdown-based faceting and searching by image file data. It ultimately uses the [astrapy](https://github.com/datastax/astrapy) library to access and work with the underlying vector embeddings in Astra DB.

## Requirements

 - A vector-enabled [Astra DB](https://astra.datastax.com) database
 - An Astra DB application token
 - An Astra DB API endpoint
 - Environment variables defined for: `FLASK_ENV`, `FLASK_APP`, ASTRA_DB_APPLICATION_TOKEN`, and `ASTRA_DB_API_ENDPOINT`:

```
export ASTRA_DB_APPLICATION_TOKEN=AstraCS:GgsdfSnotrealHqKZw:SDGSDDSG6a36d8526BLAHBLAHBLAHc18d40
export ASTRA_DB_API_ENDPOINT=https://b9aff773-also-not-real-d3088ea14425-us-east1.apps.astra.datastax.com
export FLASK_ENV=development
export FLASK_APP=crystalSearch
```

You can use a `.env` file for the vars as well.

 - A local `static/images/` directory containing JPEGs or PNGs to embed.
 - A local `static/input_images/` upload directory for JPEGs or PNGs to search _by_.
 - Python dependencies: **sentence-transformers**, **astrapy**, **flask** and **flask_wtf**. These are found in the [requirements.txt](requirements.txt) file, and can quickly be installed with the following command:

```
pip install -r requirements.txt
```

## Functionality

Descriptions and examples for each Python file in the project.

#### crystalLoader.py

 - Creates a new collection named `crystal_data`.
 - Generates embeddings for each image file.
 - Stores vector embeddings and metadata in Astra DB.

Usage:

```
python3 crystalLoader.py
```

### crystalSearch.py

 - Builds a small web frontend for the application (View).
 - Acts as the main program for the application.

Usage:

```
flask run -p 8000
```

Terminal output:

```
 * Serving Flask app 'crystalSearch'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8000
Press CTRL+C to quit
```

If you navigate in your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000), you may search in one of two ways:

 - By the dropdowns in the left navigation.
 - By image (click on the "Search" button after selecting the image).

### config.py

 - Helps configure the environment for Flask.

### webforms.py

 - A logical way to separate the web forms definitions from the main code.
 - Contains the `SearchForm`.

### crystalServices.py

 - Serves the `get_crystals_by_image` and the `get_crystals_by_facets` methods (Controller).
 - Handles all interactions with the `clip-ViT-B-32` sentence transformer.

### astraConn.py

 - Handles the connectivity with Astra DB (Model).
 - Interacts with the vector data using astrapy.
---------------------------------------------------------------------------------------------------------------------------------------
