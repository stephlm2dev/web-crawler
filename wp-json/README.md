# WP-JSON

This tool list all links/title for a Wordpress website

Based on WP-JSON API (Wordpress API)

Actually list of content types that can be fetched:
- posts
- categories
- pages
- tags

Output in CSV format

To fetch all this info, you can use:

```bash
./global.sh '<WEBSITE>' '<DIRECTORY_OUTPUT>'
```

To fetch a single type of content:

```bash
./wp-json-api.sh '<TYPE_OF_CONTENT>' '<WEBSITE>'
```
