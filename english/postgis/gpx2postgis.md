# **Extracting Spatio-Temporal Data from GPX Files**

The simplest case of spatio-temporal tables is when we assign a timestamp to point-like data.
Typically, this describes the movement of one or more moving objects. Such data can be collected with various devices; in this example, we use a Garmin recreational GNSS receiver, which outputs data in GPX format.

GPX is an international standard that stores GNSS data in XML format.

---

## **Structure of GPX Files**

GPX files can be viewed with a simple text editor.
For example, the beginning of the GPX file used in this lesson looks like this:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" ... >
```

---

## **Software Used**

During this work we use:

* PostgreSQL database system
* PostGIS spatial extension
* GDAL/OGR utilities for data conversion
* QGIS for visualization

---

## **Data**

We provide a **bicycle-recorded track** to demonstrate the workflow, but any GPX file containing a recorded track can be used.

---

## **Structure of GPX Files (Layers)**

The layers in a GPX file can be inspected using the `ogrinfo` utility (installed with GDAL/OGR):

```bash
ogrinfo god_2022.gpx
```

Example output:

```
1: waypoints (Point)
2: routes (Line String)
3: tracks (Multi Line String)
4: route_points (Point)
5: track_points (Point)
```

Not all layers are present in every GPX file.

### Layer meanings:

* **waypoints (Point)** – manually recorded points with timestamps
* **routes (LineString)** – manually created routes
* **tracks (LineString)** – automatically recorded path during movement
* **route_points (Point)** – vertices of manual routes
* **track_points (Point)** – vertices of recorded tracks with timestamps

We will use the **track_points** layer.

---

## **Inspecting the `track_points` Layer**

```bash
ogrinfo god_2022.gpx track_points
```

Example (shortened):

```
Feature Count: 3651
SRS: EPSG:4326 (WGS84)

track_fid: Integer
track_seg_id: Integer
track_seg_point_id: Integer
ele: Real
time: DateTime
```

Example records:

```
POINT (19.0417610295 47.4451178312)
time = 2022/08/05 07:01:02+00

POINT (19.0417507198 47.4451288115)
time = 2022/08/05 07:01:03+00
```

From the header we can see:

* total number of points: 3651
* coordinate system: EPSG:4326 (WGS84)

---

## **Why Use ogr2ogr**

PostGIS directly supports importing ESRI Shapefiles, but not GPX.
Therefore, we use the **ogr2ogr** utility, which supports many vector formats—including PostGIS.

---

## **Preparation in PostgreSQL**

We assume that PostGIS is already installed in the database:

```sql
CREATE EXTENSION postgis;
```

---

### **Create Sequence**

```sql
CREATE SEQUENCE IF NOT EXISTS track;
```

This sequence is used to assign a unique identifier to each imported track, so that multiple datasets can be distinguished.

---

### **Create Table**

```sql
CREATE TABLE IF NOT EXISTS test (
    tid bigint DEFAULT -1,                -- track unique id
    track_seg_point_id integer,           -- point order
    geom geometry(Point,4326) NOT NULL,   -- geometry (WGS84)
    ele double precision,                 -- elevation
    "time" timestamp with time zone,      -- timestamp
    PRIMARY KEY (tid, "time")
);
```

Notes:

* `tid` identifies individual tracks (set after import)
* Default value is `-1` to mark unassigned records
* `ogr2ogr` only imports fields that exist in the target table

---

### **Running the SQL Script**

Save the SQL commands into a file (e.g. `gpx_points2pg.sql`) and run:

```bash
psql < gpx_points2pg.sql
```

If needed, check options with:

```bash
psql --help
```

---

## **Loading Data**

After preparation, data loading is done with a single command:

```bash
ogr2ogr -update -append -f "PostgreSQL" \
PG:"host=127.0.0.1 user=xxxx dbname=xxxx password=xxxx" \
god_2022.gpx -nln test -sql "Select * From track_points"
```

Modify connection parameters accordingly.

---

## **Assign Track ID**

After loading, update the `tid` column:

```sql
SELECT nextval('track');
UPDATE test SET tid = currval('track') WHERE tid = -1;
```

---

## **Automating the Workflow**

You can combine everything into a script:

```bash
# create database objects
psql < gpx_points2pg.sql

# load GPX data
ogr2ogr -update -append -f "PostgreSQL" \
PG:"host=127.0.0.1 user=xxxx dbname=xxxx password=xxxx" \
god_2022.gpx -nln test -sql "Select * From track_points"

# update track id
psql < gpx_points2pg_post.sql
```

---

## **Final Notes**

After this, you can visualize the data using the **QGIS Temporal Controller** to explore it interactively.

You can also find guidance on connecting QGIS to PostGIS in the referenced materials.

---

