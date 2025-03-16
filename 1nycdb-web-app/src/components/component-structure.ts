// Component structure for NYCDB web application

// Main layout components
// - Header: App title, navigation, user controls
// - Sidebar: Dataset selection, filters
// - MainContent: Search interface, results display, property details
// - Footer: Links, attribution

// Page components
// - HomePage: Introduction, dataset categories, quick search
// - DatasetPage: Dataset details, search interface specific to dataset
// - PropertyPage: Comprehensive view of a property across all datasets
// - SearchResultsPage: Display and filtering of search results

// UI Components
// - DatasetSelector: Dropdown or card-based selection of datasets
// - SearchBar: Text input with field selection and submit button
// - FilterPanel: Collapsible panel with dataset-specific filters
// - ResultsTable: Paginated table of search results with sorting
// - PropertyCard: Summary card showing key property information
// - ViolationsList: List of violations with severity indicators
// - ComplaintsList: List of complaints with status indicators
// - RegistrationInfo: Display of property registration details
// - EvictionHistory: Timeline of eviction events
// - MapView: Geographic display of property or search results
// - ExportButton: Download results in CSV format

// Data visualization components
// - ViolationsByYearChart: Bar chart showing violations over time
// - ViolationsBySeverityChart: Pie chart of violations by class
// - BuildingAgeDistribution: Histogram of building ages in results
// - OwnershipNetwork: Network graph showing property ownership connections

// Utility components
// - Pagination: Controls for navigating through result pages
// - SortControls: Buttons/dropdowns for changing sort order
// - FilterChips: Visual indicators of active filters with remove option
// - LoadingSpinner: Visual indicator for async operations
// - ErrorDisplay: Formatted display of error messages
// - EmptyState: Placeholder for empty results
// - BBLInput: Specialized input for Borough-Block-Lot format
