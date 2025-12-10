import { useState, useEffect, useRef } from 'react'

function FilterBar({ filters, onFilterChange, categories }) {
    // Handler for category change
    const handleCategoryChange = (e) => {
        onFilterChange({
            ...filters,
            category: e.target.value
        })
    }

    // Handler for dateFrom
    const handleDateFromChange = (e) => {
        onFilterChange({
            ...filters,
            dateFrom: e.target.value
        })
    }

    // Handler for dateTo
    const handleDateToChange = (e) => {
        onFilterChange({
            ...filters,
            dateTo: e.target.value
        })
    }

    // Handler for min amount
    const handleMinAmount = (e) => {
        onFilterChange({
            ...filters,
            amountMin: e.target.value
        })
    }

    // Handler for max amount
    const handleMaxAmount = (e) => {
        onFilterChange({
            ...filters,
            amountMax: e.target.value
        })
    }

    // Handler for search notes
    const handleSearchNotes = (e) => {
        onFilterChange({
            ...filters,
            searchText: e.target.value
        })
    }

    // Handler for sort by
    const handleSortByChange = (e) => {
        const value = e.target.value

        if (value === 'date') {
            onFilterChange({
                ...filters,
                sortBy: 'date',
                sortOrder: 'desc'
            })
        } else if (value === 'amount-desc') {
            onFilterChange({
                ...filters,
                sortBy: 'amount',
                sortOrder: 'desc'
            })
        } else if (value === 'amount-asc') {
            onFilterChange({
                ...filters,
                sortBy: 'amount',
                sortOrder: 'asc'
    })
        }
    }

    return (
        <div className="filter-bar">

            {/* Category Filter */}
            <div className="filter-slot">
                <label>Category</label>
                <select
                    className="filter-dropdown"
                    value={filters.category}
                    onChange={handleCategoryChange}
                >
                    <option value="">All Categories</option>
                    {categories && categories
                        .filter(cat => cat.category_type === 'EXPENSE' || cat.category_type === 'INCOME')
                        .map(category => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))
                    }
                </select>
            </div>

            {/* Date From */}
            <div className="filter-slot">
                <label>From</label>
                <input type="date" value={filters.dateFrom} onChange={handleDateFromChange}
                />
            </div>

            {/* Date To */}
            <div className="filter-slot">
                <label>To</label>
                <input type="date" value={filters.dateTo} onChange={handleDateToChange} />
            </div>

            {/* Min Amount */}
            <div className="filter-slot">
                <label>Min Amount</label>
                <input type="number" value={filters.amountMin} onChange={handleMinAmount} />
            </div>

            {/* Max Amount */}
            <div className="filter-slot">
                <label>Max Amount</label>
                <input type="number" value={filters.amountMax} onChange={handleMaxAmount} />
            </div>

            {/* Search */}
            <div className="filter-slot">
                <label>Search Notes</label>
                <input type="text" value={filters.searchText} onChange={handleSearchNotes} />
            </div>

            {/* Sort By */}
            <div className="filter-slot">
                <label>Sort By</label>
                <select
                    value={filters.sortBy === 'date' ? 'date' : filters.sortBy === 'amount' ? `amount-${filters.sortOrder}` : 'date'}
                    onChange={handleSortByChange}
                >
                    <option value="date">Date</option>
                    <option value="amount-desc">Amount (High to Low)</option>
                    <option value="amount-asc">Amount (Low to High)</option>
                </select>
            </div>
        </div>
    )
}

export default FilterBar;