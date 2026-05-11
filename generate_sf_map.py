import html as _html
import json
import os

import folium
from folium.plugins import MarkerCluster
import pandas as pd

# ---------------------------------------------------------------------------
# Genre colour map
# ---------------------------------------------------------------------------
GENRE_COLORS = {
    "Drama":        "#185FA5",
    "Thriller":     "#993C1D",
    "Crime":        "#533AB7",
    "Comedy":       "#0F6E56",
    "Action":       "#BA7517",
    "Romance":      "#993556",
    "Documentary":  "#3B6D11",
    "Horror":       "#3C3489",
    "Sci-Fi":       "#5F5E5A",
    "Biography":    "#0F6E56",
    "Mystery":      "#533AB7",
    "Other":        "#888780",
}


def get_color(genre):
    for key in GENRE_COLORS:
        if key.lower() in str(genre).lower():
            return GENRE_COLORS[key]
    return GENRE_COLORS["Other"]


# ---------------------------------------------------------------------------
# Popup builder
# ---------------------------------------------------------------------------
def build_popup(row):
    poster_url = str(row.get("Poster", "") or "")
    if pd.notna(row.get("Poster")) and poster_url not in ("N/A", "", "nan"):
        poster_html = (
            f'<img src="{poster_url}" '
            f'style="width:90px;min-height:120px;object-fit:cover;flex-shrink:0;">'
        )
    else:
        poster_html = (
            '<div style="width:90px;min-height:120px;background:#e8e8e4;flex-shrink:0;'
            'display:flex;align-items:center;justify-content:center;'
            'font-size:22px;color:#aaa;">🎬</div>'
        )

    rating_val = row.get("Imdb_rating")
    rating_str = f"{float(rating_val):.1f}" if pd.notna(rating_val) else "N/A"

    year_val = row.get("Year")
    year_str = str(int(year_val)) if pd.notna(year_val) else "N/A"

    location_str     = _html.escape(str(row.get("Locations", "N/A") or "N/A"))
    neighborhood_str = _html.escape(str(row.get("Analysis neighborhood", "N/A") or "N/A"))
    director_str     = _html.escape(str(row.get("Director", "N/A") or "N/A"))
    boxing_str       = _html.escape(str(row.get("Box_office", "N/A") or "N/A"))
    title_str        = _html.escape(str(row.get("Title", "") or ""))

    sentiment_raw = str(row.get("Sentiment", "N/A") or "N/A")
    sent_color = (
        "#1D9E75" if "positive" in sentiment_raw.lower() else
        "#D85A30" if "negative" in sentiment_raw.lower() else
        "#888780"
    )

    # All-genre badges
    all_genres = row.get("All_Genres") or [row.get("Primary_Genre", "Other")]
    badges_html = ""
    for g in all_genres:
        c = get_color(g)
        badges_html += (
            f'<span style="display:inline-block;background:{c}22;'
            f'border-radius:4px;padding:2px 7px;font-size:11px;'
            f'color:{c};font-weight:500;margin:1px 2px 1px 0;">'
            f'{_html.escape(g)}</span>'
        )

    html = (
        '<div style="font-family:sans-serif;font-size:12px;width:240px;background:#fff;'
        'border-radius:10px;overflow:hidden;line-height:1.5;'
        'box-shadow:0 2px 12px rgba(0,0,0,0.12);">'

        # Header
        '<div style="display:flex;align-items:stretch;">'
        + poster_html +
        '<div style="padding:10px 12px;display:flex;flex-direction:column;'
        'justify-content:center;min-width:0;gap:4px;">'
        f'<div style="font-size:14px;font-weight:600;color:#1a1a1a;line-height:1.3;">{title_str}</div>'
        f'<div style="font-size:11px;color:#888;">{year_str}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:0;">{badges_html}</div>'
        f'<div style="display:flex;align-items:center;gap:4px;font-size:12px;">'
        '<span style="font-size:13px;">⭐</span>'
        f'<span style="font-weight:600;color:#1a1a1a;">{rating_str}</span>'
        '<span style="color:#aaa;font-size:11px;">/ 10</span>'
        '</div>'
        '</div>'
        '</div>'

        # Details grid
        '<div style="border-top:0.5px solid #eee;padding:10px 12px;'
        'display:grid;grid-template-columns:auto 1fr;gap:4px 10px;'
        'font-size:11.5px;line-height:1.5;">'

        '<span style="color:#888;white-space:nowrap;">Location</span>'
        f'<span style="color:#333;">{location_str}</span>'

        '<span style="color:#888;white-space:nowrap;">Neighborhood</span>'
        f'<span style="color:#333;">{neighborhood_str}</span>'

        '<span style="color:#888;white-space:nowrap;">Director</span>'
        f'<span style="color:#333;">{director_str}</span>'

        '<span style="color:#888;white-space:nowrap;">Box office</span>'
        f'<span style="color:#333;">{boxing_str}</span>'

        '<span style="color:#888;white-space:nowrap;">Sentiment</span>'
        '<span style="display:flex;align-items:center;gap:5px;">'
        f'<span style="display:inline-block;width:6px;height:6px;border-radius:50%;'
        f'background:{sent_color};flex-shrink:0;"></span>'
        f'<span style="color:#333;">{_html.escape(sentiment_raw)}</span>'
        '</span>'

        '</div>'
        '</div>'
    )
    return folium.Popup(html, max_width=260)


# ---------------------------------------------------------------------------
# Load & prepare
# ---------------------------------------------------------------------------
_here = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(_here, "sf_movies_cleaned_og.csv"))
df_map = df.dropna(subset=["Latitude", "Longitude"]).copy()
df_map["Primary_Genre"] = (
    df_map["Genres"].fillna("Other").str.split(",").str[0].str.strip()
)

# ---------------------------------------------------------------------------
# Map + cluster
# ---------------------------------------------------------------------------
m1 = folium.Map(
    location=[37.7749, -122.4194],
    zoom_start=12,
    tiles="CartoDB positron",
    control_scale=True,
)
cluster = MarkerCluster(
    maxClusterRadius=50,
    disableClusteringAtZoom=15,
).add_to(m1)

# ---------------------------------------------------------------------------
# Marker + record loop
# ---------------------------------------------------------------------------
records = []

for idx, (_, row) in enumerate(df_map.iterrows()):
    raw_genres = str(row.get("Genres") or "Other")
    all_genres = [g.strip() for g in raw_genres.split(",") if g.strip()]
    if not all_genres:
        all_genres = ["Other"]

    row = row.copy()
    row["All_Genres"] = all_genres

    year_val = row.get("Year")
    year     = int(year_val) if pd.notna(year_val) else None
    decade   = (year // 10 * 10) if year is not None else None

    rating_val = row.get("Imdb_rating")
    rating     = float(rating_val) if pd.notna(rating_val) else None

    box_val = None
    raw_box = str(row.get("Box_office") or "").strip()
    if raw_box and raw_box not in ("N/A", "nan"):
        try:
            box_val = int(raw_box.replace("$", "").replace(",", "").strip())
        except ValueError:
            pass

    fill_color = get_color(str(row.get("Primary_Genre", "Other")))
    marker = folium.CircleMarker(
        location=[float(row["Latitude"]), float(row["Longitude"])],
        radius=7,
        color="white",
        weight=1.5,
        fill=True,
        fill_color=fill_color,
        fill_opacity=0.85,
        popup=build_popup(row),
    )
    marker.options["filmIdx"] = idx
    marker.add_to(cluster)

    records.append({
        "idx":      idx,
        "genres":   all_genres,
        "decade":   decade,
        "rating":   rating,
        "box":      box_val,
        "lat":      float(row["Latitude"]),
        "lng":      float(row["Longitude"]),
        "title":    str(row.get("Title", "")),
        "year":     year,
        "location": str(row.get("Locations", "") or ""),
    })

# ---------------------------------------------------------------------------
# Aggregate derivation
# ---------------------------------------------------------------------------
all_genres_flat = sorted({g for r in records for g in r["genres"] if g != "Other"})
all_decades     = sorted({r["decade"] for r in records if r["decade"] is not None})
ratings_only    = [r["rating"] for r in records if r["rating"] is not None]
boxes_only      = [r["box"]    for r in records if r["box"]    is not None]
min_rating  = min(ratings_only) if ratings_only else 0.0
max_rating  = max(ratings_only) if ratings_only else 10.0
max_box     = max(boxes_only)   if boxes_only   else 0
n_no_rating = sum(1 for r in records if r["rating"] is None)
n_no_box    = sum(1 for r in records if r["box"]    is None)
total       = len(records)

# ---------------------------------------------------------------------------
# Build HTML fragments for the filter panel
# ---------------------------------------------------------------------------
genre_chips_html = ""
for g in all_genres_flat:
    c = get_color(g)
    genre_chips_html += (
        '<div class="chip genre-chip"'
        f' data-genre="{_html.escape(g)}" data-color="{c}"'
        ' style="display:inline-flex;align-items:center;gap:5px;cursor:pointer;'
        'padding:4px 10px;border-radius:20px;margin:2px;font-size:12px;'
        'border:1px solid #e0ddd6;background:#f7f6f3;color:#444;user-select:none;">'
        f'<span style="width:7px;height:7px;border-radius:50%;background:{c};'
        f'flex-shrink:0;"></span>{_html.escape(g)}</div>'
    )

decade_chips_html = ""
for d in all_decades:
    decade_chips_html += (
        '<div class="chip decade-chip"'
        f' data-decade="{d}"'
        ' style="display:inline-flex;align-items:center;cursor:pointer;'
        'padding:4px 10px;border-radius:20px;margin:2px;font-size:12px;'
        'border:1px solid #e0ddd6;background:#f7f6f3;color:#444;user-select:none;">'
        f'{d}s</div>'
    )

no_rating_cb = (
    '<label style="display:flex;align-items:center;gap:6px;font-size:11.5px;'
    'color:#666;margin-top:4px;cursor:pointer;">'
    '<input type="checkbox" id="include-no-rating" checked style="cursor:pointer;">'
    f'Include unrated ({n_no_rating} films)</label>'
) if n_no_rating > 0 else ""

no_box_cb = (
    '<label style="display:flex;align-items:center;gap:6px;font-size:11.5px;'
    'color:#666;margin-top:4px;cursor:pointer;">'
    '<input type="checkbox" id="include-no-box" checked style="cursor:pointer;">'
    f'Include unreported ({n_no_box} films)</label>'
) if n_no_box > 0 else ""

records_json = json.dumps(records, ensure_ascii=False)

# ---------------------------------------------------------------------------
# Filter panel HTML  (JS braces escaped as {{ / }} inside the f-string)
# ---------------------------------------------------------------------------
filter_panel_html = f"""
<!-- SF Map title banner -->
<div style="position:fixed;top:12px;left:50%;transform:translateX(-50%);
            z-index:1000;background:rgba(255,255,255,0.92);padding:7px 18px;
            border-radius:20px;border:0.5px solid #e0ddd6;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
            font-family:sans-serif;font-size:13px;font-weight:600;
            color:#1a1a1a;pointer-events:none;white-space:nowrap;">
  San Francisco Filming Locations
  <span style="font-weight:400;color:#888;">&nbsp;&middot; click a marker to explore</span>
</div>

<!-- Filter panel -->
<div id="filter-panel"
     style="position:fixed;top:12px;right:16px;width:288px;z-index:1000;
            background:#fff;border:0.5px solid #e0ddd6;border-radius:12px;
            box-shadow:0 4px 20px rgba(0,0,0,0.10);font-family:sans-serif;">

  <!-- Header -->
  <div style="display:flex;align-items:center;justify-content:space-between;
              padding:12px 16px 10px;border-bottom:0.5px solid #ece9e1;">
    <span style="font-size:13px;font-weight:700;color:#1a1a1a;">Filters</span>
    <div style="display:flex;align-items:center;gap:10px;">
      <span id="match-count"
            style="font-size:11.5px;color:#888;background:#f2f0eb;
                   padding:2px 8px;border-radius:10px;">{total} films</span>
      <button onclick="resetFilters()"
              style="font-size:12px;color:#888;background:none;
                     border:none;cursor:pointer;padding:0;">reset</button>
    </div>
  </div>

  <!-- Filter sections -->
  <div style="padding:12px 16px;display:flex;flex-direction:column;gap:14px;
              max-height:calc(100vh - 120px);overflow-y:auto;">

    <!-- Genre -->
    <div>
      <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.06em;
                  color:#aaa;font-weight:600;margin-bottom:6px;">Genre</div>
      <div id="genre-chips" style="display:flex;flex-wrap:wrap;gap:0;">
        {genre_chips_html}
      </div>
    </div>

    <!-- Decade -->
    <div>
      <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.06em;
                  color:#aaa;font-weight:600;margin-bottom:6px;">Decade</div>
      <div id="decade-chips" style="display:flex;flex-wrap:wrap;gap:0;">
        {decade_chips_html}
      </div>
    </div>

    <!-- IMDb Rating -->
    <div>
      <div style="display:flex;justify-content:space-between;align-items:center;
                  margin-bottom:4px;">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.06em;
                    color:#aaa;font-weight:600;">IMDb Rating</div>
        <span id="rating-display" style="font-size:11.5px;color:#666;"></span>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <input type="range" id="rating-min"
               min="{min_rating}" max="{max_rating}" step="0.1" value="{min_rating}"
               style="flex:1;accent-color:#1a1a1a;">
        <input type="range" id="rating-max"
               min="{min_rating}" max="{max_rating}" step="0.1" value="{max_rating}"
               style="flex:1;accent-color:#1a1a1a;">
      </div>
      {no_rating_cb}
    </div>

    <!-- Box Office -->
    <div>
      <div style="display:flex;justify-content:space-between;align-items:center;
                  margin-bottom:4px;">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.06em;
                    color:#aaa;font-weight:600;">Box Office</div>
        <span id="box-display" style="font-size:11.5px;color:#666;"></span>
      </div>
      <input type="range" id="box-min"
             min="0" max="{max_box}" step="1000000" value="0"
             style="width:100%;accent-color:#1a1a1a;">
      {no_box_cb}
    </div>

  </div>
</div>

<script>
(function () {{
  /* ---- data ---- */
  var RECORDS = {records_json};

  /* ---- filter state ---- */
  var activeGenres  = {{}};
  var activeDecades = {{}};
  var ratingMin = {min_rating};
  var ratingMax = {max_rating};
  var boxMin    = 0;
  var includeNoRating = true;
  var includeNoBox    = true;

  /* ---- marker registry ---- */
  var markerByIdx = {{}};
  var inCluster   = {{}};
  var mcgLayer    = null;

  /* ---- helpers to locate Folium objects ---- */
  function findLeafMap() {{
    for (var k in window) {{
      try {{
        if (k.indexOf('map_') === 0 &&
            window[k] != null &&
            typeof window[k].eachLayer === 'function')
          return window[k];
      }} catch (e) {{}}
    }}
    return null;
  }}

  function findCluster(leafMap) {{
    var found = null;
    leafMap.eachLayer(function (layer) {{
      if (!found &&
          typeof layer.addLayers    === 'function' &&
          typeof layer.removeLayers === 'function')
        found = layer;
    }});
    return found;
  }}

  /* ---- bootstrap: run after window load ---- */
  function bootstrap() {{
    var leafMap = findLeafMap();
    if (!leafMap) {{ setTimeout(bootstrap, 200); return; }}
    mcgLayer = findCluster(leafMap);
    if (!mcgLayer) {{ setTimeout(bootstrap, 200); return; }}

    mcgLayer.eachLayer(function (marker) {{
      var idx = marker.options && marker.options.filmIdx;
      if (idx !== undefined && idx !== null) {{
        markerByIdx[idx] = marker;
        inCluster[idx]   = true;
      }}
    }});

    updateDisplays();
    applyFilters();
  }}

  /* ---- filter predicate ---- */
  function passes(rec) {{
    /* Genre: pass if any active genre appears in rec.genres */
    var gKeys = Object.keys(activeGenres);
    if (gKeys.length > 0) {{
      var hit = false;
      for (var i = 0; i < rec.genres.length; i++) {{
        if (activeGenres[rec.genres[i]]) {{ hit = true; break; }}
      }}
      if (!hit) return false;
    }}

    /* Decade: null always fails when a filter is active */
    var dKeys = Object.keys(activeDecades);
    if (dKeys.length > 0) {{
      if (rec.decade === null || rec.decade === undefined) return false;
      if (!activeDecades[rec.decade]) return false;
    }}

    /* Rating */
    if (rec.rating === null || rec.rating === undefined) {{
      if (!includeNoRating) return false;
    }} else {{
      if (rec.rating < ratingMin || rec.rating > ratingMax) return false;
    }}

    /* Box office */
    if (rec.box === null || rec.box === undefined) {{
      if (!includeNoBox) return false;
    }} else {{
      if (rec.box < boxMin) return false;
    }}

    return true;
  }}

  /* ---- apply filters: batch add / remove ---- */
  function applyFilters() {{
    if (!mcgLayer) return;
    var toAdd    = [];
    var toRemove = [];
    var count    = 0;
    var idxKeys  = Object.keys(markerByIdx);

    for (var i = 0; i < idxKeys.length; i++) {{
      var idx = parseInt(idxKeys[i], 10);
      var rec = RECORDS[idx];
      if (!rec) continue;
      var show = passes(rec);
      if (show) count++;
      if (show && !inCluster[idx]) {{
        toAdd.push(markerByIdx[idx]);
        inCluster[idx] = true;
      }} else if (!show && inCluster[idx]) {{
        toRemove.push(markerByIdx[idx]);
        inCluster[idx] = false;
      }}
    }}

    if (toRemove.length) mcgLayer.removeLayers(toRemove);
    if (toAdd.length)    mcgLayer.addLayers(toAdd);
    document.getElementById('match-count').textContent = count + ' films';
  }}

  /* ---- update slider display labels ---- */
  function updateDisplays() {{
    document.getElementById('rating-display').textContent =
      ratingMin.toFixed(1) + ' – ' + ratingMax.toFixed(1);
    var bM = Math.round(boxMin / 1e6);
    document.getElementById('box-display').textContent =
      boxMin === 0 ? '$0' : ('$' + bM + 'M+');
  }}

  /* ---- reset (exposed globally) ---- */
  window.resetFilters = function () {{
    activeGenres  = {{}};
    activeDecades = {{}};
    ratingMin = {min_rating};
    ratingMax = {max_rating};
    boxMin    = 0;
    includeNoRating = true;
    includeNoBox    = true;

    document.querySelectorAll('.genre-chip').forEach(function (el) {{
      var c = el.getAttribute('data-color');
      el.style.background = '#f7f6f3';
      el.style.color      = '#444';
      el.style.border     = '1px solid #e0ddd6';
      el.querySelector('span').style.background = c;
    }});
    document.querySelectorAll('.decade-chip').forEach(function (el) {{
      el.style.background = '#f7f6f3';
      el.style.color      = '#444';
      el.style.border     = '1px solid #e0ddd6';
    }});

    var rMinEl = document.getElementById('rating-min');
    var rMaxEl = document.getElementById('rating-max');
    if (rMinEl) rMinEl.value = {min_rating};
    if (rMaxEl) rMaxEl.value = {max_rating};

    var bMinEl = document.getElementById('box-min');
    if (bMinEl) bMinEl.value = 0;

    var cb1 = document.getElementById('include-no-rating');
    var cb2 = document.getElementById('include-no-box');
    if (cb1) cb1.checked = true;
    if (cb2) cb2.checked = true;

    updateDisplays();
    applyFilters();
  }};

  /* ---- wire up UI after DOM ready ---- */
  window.addEventListener('load', function () {{

    /* Genre chips */
    document.querySelectorAll('.genre-chip').forEach(function (el) {{
      el.addEventListener('click', function () {{
        var g = el.getAttribute('data-genre');
        var c = el.getAttribute('data-color');
        if (activeGenres[g]) {{
          delete activeGenres[g];
          el.style.background = '#f7f6f3';
          el.style.color      = '#444';
          el.style.border     = '1px solid #e0ddd6';
          el.querySelector('span').style.background = c;
        }} else {{
          activeGenres[g]     = true;
          el.style.background = c;
          el.style.color      = '#fff';
          el.style.border     = '1px solid ' + c;
          el.querySelector('span').style.background = '#fff';
        }}
        applyFilters();
      }});
    }});

    /* Decade chips */
    document.querySelectorAll('.decade-chip').forEach(function (el) {{
      el.addEventListener('click', function () {{
        var d = parseInt(el.getAttribute('data-decade'), 10);
        if (activeDecades[d]) {{
          delete activeDecades[d];
          el.style.background = '#f7f6f3';
          el.style.color      = '#444';
          el.style.border     = '1px solid #e0ddd6';
        }} else {{
          activeDecades[d]    = true;
          el.style.background = '#1a1a1a';
          el.style.color      = '#fff';
          el.style.border     = '1px solid #1a1a1a';
        }}
        applyFilters();
      }});
    }});

    /* Rating sliders with cross-validation */
    var rMinEl = document.getElementById('rating-min');
    var rMaxEl = document.getElementById('rating-max');
    if (rMinEl) {{
      rMinEl.addEventListener('input', function () {{
        ratingMin = parseFloat(this.value);
        if (ratingMin > ratingMax) {{
          ratingMax      = ratingMin;
          rMaxEl.value   = ratingMax;
        }}
        updateDisplays();
        applyFilters();
      }});
    }}
    if (rMaxEl) {{
      rMaxEl.addEventListener('input', function () {{
        ratingMax = parseFloat(this.value);
        if (ratingMax < ratingMin) {{
          ratingMin      = ratingMax;
          rMinEl.value   = ratingMin;
        }}
        updateDisplays();
        applyFilters();
      }});
    }}

    /* Box office slider */
    var bMinEl = document.getElementById('box-min');
    if (bMinEl) {{
      bMinEl.addEventListener('input', function () {{
        boxMin = parseInt(this.value, 10);
        updateDisplays();
        applyFilters();
      }});
    }}

    /* Checkboxes */
    var cb1 = document.getElementById('include-no-rating');
    var cb2 = document.getElementById('include-no-box');
    if (cb1) cb1.addEventListener('change', function () {{
      includeNoRating = this.checked; applyFilters();
    }});
    if (cb2) cb2.addEventListener('change', function () {{
      includeNoBox = this.checked; applyFilters();
    }});

    bootstrap();
  }});

}})();
</script>
"""

# ---------------------------------------------------------------------------
# Inject & save
# ---------------------------------------------------------------------------
m1.get_root().html.add_child(folium.Element(""))   # empty legend slot
m1.get_root().html.add_child(folium.Element(filter_panel_html))
m1.save(os.path.join(_here, "sf_map_clustered3.html"))
print("Saved sf_map_clustered3.html")
