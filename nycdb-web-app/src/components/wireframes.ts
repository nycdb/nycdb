// Wireframes for NYCDB Web Application

/*
HOME PAGE WIREFRAME
------------------
+-------------------------------------------------------+
| NYCDB Web App                           [About] [Help] |
+-------------------------------------------------------+
|                                                       |
|  Welcome to NYCDB Web Application                     |
|                                                       |
|  Explore NYC housing data from multiple sources       |
|                                                       |
|  +-------------------+  +-------------------+         |
|  | Property Data     |  | Violations        |         |
|  | - PLUTO           |  | - HPD Violations  |         |
|  | - HPD Registrations|  | - DOB Violations |         |
|  +-------------------+  +-------------------+         |
|                                                       |
|  +-------------------+  +-------------------+         |
|  | Complaints        |  | Evictions         |         |
|  | - DOB Complaints  |  | - Marshal         |         |
|  | - HPD Complaints  |  |   Evictions       |         |
|  +-------------------+  +-------------------+         |
|                                                       |
|  Quick Search:                                        |
|  +-----------------------------------------------+    |
|  | Enter address, BBL, or building info    [Search]   |
|  +-----------------------------------------------+    |
|                                                       |
+-------------------------------------------------------+
| Footer: Data provided by NYCDB | Housing Data Coalition |
+-------------------------------------------------------+

DATASET PAGE WIREFRAME
---------------------
+-------------------------------------------------------+
| NYCDB Web App                   [Datasets] [About]    |
+-------------------------------------------------------+
| < Back to Datasets                                    |
|                                                       |
| HPD Violations                                        |
| Housing violations issued by the Department of        |
| Housing Preservation and Development                  |
|                                                       |
| Search:                                               |
| +------------------------+ +----------+ +---------+   |
| | Enter search term      | |Field ▼   | |Search   |   |
| +------------------------+ +----------+ +---------+   |
|                                                       |
| Filters:                                              |
| +------------+  +------------+  +------------+        |
| |Borough ▼   |  |Class ▼     |  |Status ▼    |        |
| +------------+  +------------+  +------------+        |
|                                                       |
| Date Range:                                           |
| +------------+  +------------+                        |
| |From        |  |To          |                        |
| +------------+  +------------+                        |
|                                                       |
| Results: 0 found                                      |
|                                                       |
| +-----------------------------------------------+     |
| | ID | Address | Class | Issue Date | Status    |     |
| |----+---------|-------|------------|-----------|     |
| |    |         |       |            |           |     |
| |    |         |       |            |           |     |
| |    |         |       |            |           |     |
| +-----------------------------------------------+     |
|                                                       |
| [< Prev] Page 1 of 0 [Next >]        [Export CSV]     |
|                                                       |
+-------------------------------------------------------+
| Footer: Data provided by NYCDB | Housing Data Coalition |
+-------------------------------------------------------+

PROPERTY DETAIL WIREFRAME
------------------------
+-------------------------------------------------------+
| NYCDB Web App                   [Datasets] [About]    |
+-------------------------------------------------------+
| < Back to Search Results                              |
|                                                       |
| 123 Main Street, Manhattan (BBL: 1-00123-0045)        |
|                                                       |
| +-------------------+  +------------------------+     |
| | Property Info     |  |       Building Map     |     |
| | Borough: Manhattan|  |                        |     |
| | Block: 123        |  |                        |     |
| | Lot: 45           |  |                        |     |
| | Year Built: 1930  |  |                        |     |
| | Units: 24         |  |                        |     |
| +-------------------+  +------------------------+     |
|                                                       |
| +-----------------------------------------------+     |
| | Tabs: Overview | Violations | Complaints | Evictions |
| +-----------------------------------------------+     |
| |                                               |     |
| | HPD Violations: 12 open, 45 total             |     |
| |                                               |     |
| | Recent Violations:                            |     |
| | - Class C: No heat (Jan 15, 2025)             |     |
| | - Class B: Peeling paint (Dec 3, 2024)        |     |
| | - Class A: Smoke detector (Nov 10, 2024)      |     |
| |                                               |     |
| | [View All Violations]                         |     |
| |                                               |     |
| | DOB Complaints: 3 open, 8 total               |     |
| |                                               |     |
| | Recent Complaints:                            |     |
| | - Illegal construction (Feb 2, 2025)          |     |
| | - Elevator not working (Jan 5, 2025)          |     |
| |                                               |     |
| | [View All Complaints]                         |     |
| |                                               |     |
| +-----------------------------------------------+     |
|                                                       |
+-------------------------------------------------------+
| Footer: Data provided by NYCDB | Housing Data Coalition |
+-------------------------------------------------------+

SEARCH RESULTS WIREFRAME
-----------------------
+-------------------------------------------------------+
| NYCDB Web App                   [Datasets] [About]    |
+-------------------------------------------------------+
| < Back to HPD Violations                              |
|                                                       |
| Search Results: "no heat" in HPD Violations           |
|                                                       |
| Filters: Class C | Manhattan | Open                   |
|                                                       |
| 245 results found                                     |
|                                                       |
| Sort by: [Date ▼]                                     |
|                                                       |
| +-----------------------------------------------+     |
| | Address         | Issue Date | Status | Class |     |
| |-----------------|------------|--------|-------|     |
| | 123 Main St     | 01/15/2025 | Open   | C     |     |
| | 456 Broadway    | 01/12/2025 | Open   | C     |     |
| | 789 West End Ave| 01/10/2025 | Open   | C     |     |
| | 321 Park Ave    | 01/05/2025 | Open   | C     |     |
| | 654 5th Ave     | 12/28/2024 | Open   | C     |     |
| | 987 Madison Ave | 12/22/2024 | Open   | C     |     |
| | 234 E 86th St   | 12/18/2024 | Open   | C     |     |
| | 567 W 125th St  | 12/15/2024 | Open   | C     |     |
| | 890 Amsterdam   | 12/10/2024 | Open   | C     |     |
| | 432 Lenox Ave   | 12/05/2024 | Open   | C     |     |
| +-----------------------------------------------+     |
|                                                       |
| [< Prev] Page 1 of 25 [Next >]       [Export CSV]     |
|                                                       |
+-------------------------------------------------------+
| Footer: Data provided by NYCDB | Housing Data Coalition |
+-------------------------------------------------------+
*/
