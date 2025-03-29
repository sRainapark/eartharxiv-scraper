
# 🌍 EarthArXiv Preprint Scraper

This project scrapes metadata from EarthArXiv preprints related to **climate** research. It collects data directly from preprint detail pages (`/repository/view/{id}/`) and extracts key metadata using `<meta>` tags. The script is designed to help researchers, educators, and developers collect openly licensed academic content for analysis or downstream use.

---

## Features

- **Keyword Filtering** — Only collects papers that mention `"climate"` in their title or abstract.
- **Metadata Extraction** — Grabs title, abstract, authors, license, publication date, DOI, and URL.
- **License Filtering** — Includes only papers with open Creative Commons licenses (`CC BY`, `CC BY-NC`, `CC BY-SA`).
- **Publication Date Filter** — Filters out papers published before 2015.
- **Author Limit Filter** — Limits to a maximum of 5 papers per author.
- **CSV Output** — Saves results to `eartharxiv_climate_preprints.csv`.

---

## Installation

This project is designed to run in **Google Colab**, but you can also run it locally in a Python 3 environment.

Install the required packages (in Colab or locally):

```bash
pip install beautifulsoup4 tqdm
```

---

## How to Use

Just copy and paste the full script into a Colab notebook and run. The script will:

- Randomly sample preprint IDs (from `view/1000` to `view/12000`)
- Collect up to 600 matching preprints
- Save results to a CSV
- Let you download the CSV directly from Colab

### Customization

You can easily change these parameters in the config section of the script:

| Parameter | What It Does | How to Change |
| --- | --- | --- |
| `KEYWORD` | Filter by different topic (e.g. `"geology"`, `"carbon"`) | Set to your desired string |
| `MAX_PREPRINTS` | Number of papers to collect | Increase/decrease this number |
| `MIN_YEAR` | Only collect papers published after this year | Change to e.g. `2010` |
| `START_ID`, `END_ID` | ID range to sample from | Use a wider range for more coverage |
| `ACCEPTED_LICENSES` | Allowed license types | Add/remove license types |
| `MAX_PAPERS_PER_AUTHOR` | Limit how many papers one author can appear in | Adjust to prevent over-representation |

---

## Example

Collect 300 preprints related to `"geology"` from EarthArXiv:

```python
KEYWORD = "geology"
MAX_PREPRINTS = 300
```

Collect 800 `"climate"` papers from a broader ID range:

```python
START_ID = 1000
END_ID = 15000
MAX_PREPRINTS = 800
KEYWORD = "climate"
```

---

## Output

The script saves a file named:

```
eartharxiv_climate_preprints.csv
```

With the following columns:

- Title
- Authors
- DOI
- License
- Abstract
- URL
- Publication Date

If you'd rather **store it to Google Drive** instead of downloading every time, do this:

1. **Mount Google Drive**

```python
from google.colab import drive
drive.mount('/content/drive')
```

Then approve access to your Google Drive.

2. **Move the CSV to Your Drive**

```python
!mv eartharxiv_environmental_sciences.csv /content/drive/MyDrive/
```

You'll now find the file in your Google Drive under `MyDrive`.

---

## Efficiency & Performance

### Expected Runtime

This scraper samples EarthArXiv preprints one by one from `https://eartharxiv.org/repository/view/{id}/`. Because not every ID leads to a valid or matching preprint (due to filters), it may need to probe **thousands of pages** to collect your full sample.

- **600 preprints** typically takes **15–30 minutes** on Colab
- Time depends on:
    - Number of invalid IDs (nonexistent or don't match filters)
    - Network speed
    - `SLEEP_BETWEEN` delay (default: 1 sec)

### Tips to Improve Efficiency

| Tip | Description |
| --- | --- |
| **Lower `SLEEP_BETWEEN`** | You can set it to `0.2` or `0.5` instead of `1` to speed up scraping. Just don't hammer the site. |
| **Increase `START_ID`/`END_ID` Range** | A wider range increases your chances of finding valid papers faster. Try `1000–15000`. |
| **Relax Filters** | Allow older papers (`MIN_YEAR = 2010`) or allow more per author (`MAX_PAPERS_PER_AUTHOR = 10`). |
| **Reduce Sample Size** | If you only need 100–200 preprints, set `MAX_PREPRINTS = 200` for a much faster run. |
| **Cache & Resume** | Add code to save progress and resume if interrupted (can be added if needed). |

---

## Use Cases

- Build datasets for NLP, citation analysis, or climate policy research
- Power open-access literature discovery tools
- Collect abstracts for machine learning or keyword extraction

---

## 📝 License

This scraper only collects **openly licensed** preprints under Creative Commons terms.

 (Initial commit: scraper, README, requirements)
