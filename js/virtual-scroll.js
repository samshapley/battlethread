/**
 * Virtual Scrolling Implementation for BattleThread Timeline
 * Handles variable heights for different item types
 */

class VirtualScroller {
    constructor(options) {
        this.container = options.container;
        this.items = options.items || [];
        this.renderItem = options.renderItem;
        this.bufferSize = options.bufferSize || 30;
        
        // Different heights for different item types
        this.itemHeights = {
            battle: 24,
            century: 30
        };
        
        this.scrollTop = 0;
        this.visibleStart = 0;
        this.visibleEnd = 0;
        this.renderedElements = new Map();
        this.itemPositions = [];
        
        this.init();
    }
    
    init() {
        // Get the timeline items container
        this.itemsContainer = document.getElementById('timelineItems');
        
        // Calculate positions for all items based on their actual heights
        this.calculateItemPositions();
        
        // Set the total height for proper scrollbar
        const totalHeight = this.itemPositions.length > 0 
            ? this.itemPositions[this.itemPositions.length - 1].bottom 
            : 0;
        this.itemsContainer.style.height = `${totalHeight}px`;
        this.itemsContainer.style.position = 'relative';
        
        // Add scroll listener with throttling
        let scrollTimeout;
        this.container.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.onScroll();
            }, 10);
        });
        
        // Initial render
        this.render();
    }
    
    calculateItemPositions() {
        this.itemPositions = [];
        let currentTop = 0;
        
        for (let i = 0; i < this.items.length; i++) {
            const item = this.items[i];
            const height = this.itemHeights[item.type] || 24;
            
            this.itemPositions.push({
                index: i,
                top: currentTop,
                bottom: currentTop + height,
                height: height
            });
            
            currentTop += height;
            
            // Add 2px gap after century markers to prevent overlap with next item
            if (item.type === 'century') {
                currentTop += 2;
            }
        }
    }
    
    findVisibleItems(scrollTop, containerHeight) {
        const viewportTop = scrollTop;
        const viewportBottom = scrollTop + containerHeight;
        
        let startIndex = 0;
        let endIndex = this.itemPositions.length - 1;
        
        // Binary search for the first visible item
        for (let i = 0; i < this.itemPositions.length; i++) {
            if (this.itemPositions[i].bottom >= viewportTop) {
                startIndex = Math.max(0, i - this.bufferSize);
                break;
            }
        }
        
        // Find the last visible item
        for (let i = startIndex; i < this.itemPositions.length; i++) {
            if (this.itemPositions[i].top > viewportBottom) {
                endIndex = Math.min(this.itemPositions.length - 1, i + this.bufferSize);
                break;
            }
        }
        
        return { startIndex, endIndex };
    }
    
    onScroll() {
        this.scrollTop = this.container.scrollTop;
        this.render();
    }
    
    render() {
        const containerHeight = this.container.clientHeight;
        const { startIndex, endIndex } = this.findVisibleItems(this.scrollTop, containerHeight);
        
        this.visibleStart = startIndex;
        this.visibleEnd = endIndex + 1;
        
        // Track which elements to keep
        const elementsToKeep = new Set();
        
        // Render visible items
        for (let i = this.visibleStart; i < this.visibleEnd && i < this.items.length; i++) {
            const item = this.items[i];
            const position = this.itemPositions[i];
            const key = `${item.type}-${i}`;
            elementsToKeep.add(key);
            
            // Check if element already exists
            let element = this.renderedElements.get(key);
            if (!element) {
                element = this.renderItem(item, i);
                this.itemsContainer.appendChild(element);
                this.renderedElements.set(key, element);
            }
            
            // Update position with correct height
            element.style.position = 'absolute';
            element.style.top = `${position.top}px`;
            element.style.left = '0';
            element.style.right = '0';
            element.style.height = `${position.height}px`;
        }
        
        // Remove elements that are no longer visible
        for (const [key, element] of this.renderedElements) {
            if (!elementsToKeep.has(key)) {
                element.remove();
                this.renderedElements.delete(key);
            }
        }
    }
    
    updateItems(items) {
        // Clear all rendered elements
        for (const [key, element] of this.renderedElements) {
            element.remove();
        }
        this.renderedElements.clear();
        
        // Update items
        this.items = items;
        
        // Recalculate positions
        this.calculateItemPositions();
        
        // Update container height
        const totalHeight = this.itemPositions.length > 0 
            ? this.itemPositions[this.itemPositions.length - 1].bottom 
            : 0;
        this.itemsContainer.style.height = `${totalHeight}px`;
        
        // Render new items
        this.render();
    }
    
    scrollToItem(index) {
        if (index >= 0 && index < this.itemPositions.length) {
            const scrollTop = this.itemPositions[index].top;
            this.container.scrollTop = scrollTop;
        }
    }
    
    getVisibleRange() {
        return {
            start: this.visibleStart,
            end: this.visibleEnd
        };
    }
}

// Century grouping helper
function groupBattlesByCentury(battles) {
    const groups = [];
    let currentCentury = null;
    
    battles.forEach((battle, index) => {
        const year = battle.date.year;
        const century = Math.floor(Math.abs(year) / 100) * 100 * (year < 0 ? -1 : 1);
        
        if (century !== currentCentury) {
            currentCentury = century;
            groups.push({
                type: 'century',
                century: century,
                text: formatCentury(century),
                originalIndex: index
            });
        }
        
        groups.push({
            type: 'battle',
            data: battle,
            originalIndex: index
        });
    });
    
    return groups;
}

function formatCentury(century) {
    if (century < 0) {
        return `${Math.abs(century)}s BC`;
    } else if (century === 0) {
        return '1st Century';
    } else {
        const centuryNum = Math.floor(century / 100) + 1;
        const suffix = centuryNum === 1 ? 'st' : centuryNum === 2 ? 'nd' : centuryNum === 3 ? 'rd' : 'th';
        return `${centuryNum}${suffix} Century`;
    }
}

// Export for use in timeline.js
window.VirtualScroller = VirtualScroller;
window.groupBattlesByCentury = groupBattlesByCentury;