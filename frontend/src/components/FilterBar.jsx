import { useState, useEffect, useRef } from 'react'

function FilterBar({ filters, onFilterChange, categories }) {
    // Handler for category change
    const handleCategoryChange = (e) => {
        onFilterChange({
            ...filters,
            category: e.target.value
        })
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
                        .filter(cat => cat.category_type === 'expense')
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
                <input type="date" />
            </div>

            {/* Date To */}
            <div className="filter-slot">
                <label>To</label>
                <input type="date" />
            </div>

            {/* Min Amount */}
            <div className="filter-slot">
                <label>Min Amount</label>
                <input type="number" />
            </div>

            {/* Max Amount */}
            <div className="filter-slot">
                <label>Max Amount</label>
                <input type="number" />
            </div>

            {/* Search */}
            <div className="filter-slot">
                <label>Search Notes</label>
                <input type="text" />
            </div>

            {/* Sort */}
            <div className="filter-slot">
                <label>Sort By</label>
                <select>...</select>
            </div>
        </div>
    )
}

export default FilterBar;