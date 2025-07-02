/**
 * BattleThread Timeline - Main Application Logic
 */

class Timeline {
    constructor() {
        this.battles = [];
        this.filteredBattles = [];
        this.selectedBattle = null;
        this.virtualScroller = null;
        
        this.init();
    }
    
    async init() {
        // Show loading state
        this.showLoading();
        
        // Load battle data
        await this.loadBattleData();
        
        // Initialize UI components
        this.initializeTimeline();
        this.initializeSearch();
        this.initializeMinimap();
        
        // Update battle count
        this.updateBattleCount();
    }
    
    showLoading() {
        const container = document.getElementById('timelineItems');
        container.innerHTML = '<div class="loading">Loading battles...</div>';
    }
    
    async loadBattleData() {
        try {
            const response = await fetch('data/battles_timeline.json');
            const data = await response.json();
            
            this.battles = data.battles;
            this.filteredBattles = [...this.battles];
            
            console.log(`Loaded ${this.battles.length} battles`);
            console.log(`Date range: ${data.metadata.dateRange.earliest} to ${data.metadata.dateRange.latest}`);
            
        } catch (error) {
            console.error('Error loading battle data:', error);
            // For demo, create sample data if file not found
            this.createSampleData();
        }
    }
    
    createSampleData() {
        // Create sample battles for demo if data file not found
        const sampleBattles = [
            { id: 'marathon', name: 'Battle of Marathon', date: { year: -490, display: '490 BC', sortKey: 9510, confidence: 'high' }},
            { id: 'thermopylae', name: 'Battle of Thermopylae', date: { year: -480, display: '480 BC', sortKey: 9520, confidence: 'high' }},
            { id: 'salamis', name: 'Battle of Salamis', date: { year: -480, display: '480 BC', sortKey: 9520, confidence: 'high' }},
            { id: 'gaugamela', name: 'Battle of Gaugamela', date: { year: -331, display: '331 BC', sortKey: 9669, confidence: 'high' }},
            { id: 'cannae', name: 'Battle of Cannae', date: { year: -216, display: '216 BC', sortKey: 9784, confidence: 'high' }},
            { id: 'actium', name: 'Battle of Actium', date: { year: -31, display: '31 BC', sortKey: 9969, confidence: 'high' }},
            { id: 'teutoburg', name: 'Battle of the Teutoburg Forest', date: { year: 9, display: '9 AD', sortKey: 10009, confidence: 'high' }},
            { id: 'tours', name: 'Battle of Tours', date: { year: 732, display: '732', sortKey: 10732, confidence: 'high' }},
            { id: 'hastings', name: 'Battle of Hastings', date: { year: 1066, display: '14 October 1066', sortKey: 11066, confidence: 'high' }},
            { id: 'agincourt', name: 'Battle of Agincourt', date: { year: 1415, display: '25 October 1415', sortKey: 11415, confidence: 'high' }},
            { id: 'vienna', name: 'Battle of Vienna', date: { year: 1683, display: '12 September 1683', sortKey: 11683, confidence: 'high' }},
            { id: 'waterloo', name: 'Battle of Waterloo', date: { year: 1815, display: '18 June 1815', sortKey: 11815, confidence: 'high' }},
            { id: 'gettysburg', name: 'Battle of Gettysburg', date: { year: 1863, display: '1-3 July 1863', sortKey: 11863, confidence: 'high' }},
            { id: 'verdun', name: 'Battle of Verdun', date: { year: 1916, display: '21 February 1916', sortKey: 11916, confidence: 'high' }},
            { id: 'stalingrad', name: 'Battle of Stalingrad', date: { year: 1942, display: '23 August 1942', sortKey: 11942, confidence: 'high' }},
            { id: 'midway', name: 'Battle of Midway', date: { year: 1942, display: '4-7 June 1942', sortKey: 11942, confidence: 'high' }},
            { id: 'normandy', name: 'Battle of Normandy', date: { year: 1944, display: '6 June 1944', sortKey: 11944, confidence: 'high' }}
        ];
        
        // Generate more sample data
        for (let year = -500; year <= 2000; year += 50) {
            if (Math.random() > 0.3) {
                sampleBattles.push({
                    id: `battle_${year}`,
                    name: `Sample Battle of ${Math.abs(year)}`,
                    date: {
                        year: year,
                        display: year < 0 ? `${Math.abs(year)} BC` : `${year}`,
                        sortKey: year + 10000,
                        confidence: 'medium'
                    }
                });
            }
        }
        
        this.battles = sampleBattles.sort((a, b) => a.date.sortKey - b.date.sortKey);
        this.filteredBattles = [...this.battles];
    }
    
    initializeTimeline() {
        const container = document.getElementById('timelineContainer');
        const itemsContainer = document.getElementById('timelineItems');
        
        // Clear loading state
        itemsContainer.innerHTML = '';
        
        // Group battles by century
        const groupedItems = groupBattlesByCentury(this.filteredBattles);
        
        // Initialize virtual scroller
        this.virtualScroller = new VirtualScroller({
            container: container,
            items: groupedItems,
            itemHeight: 24,
            bufferSize: 30,
            renderItem: (item, index) => this.renderTimelineItem(item, index)
        });
    }
    
    renderTimelineItem(item, index) {
        if (item.type === 'century') {
            return this.renderCenturyMarker(item);
        } else {
            return this.renderBattleItem(item.data, index);
        }
    }
    
    renderCenturyMarker(item) {
        const div = document.createElement('div');
        div.className = 'century-marker';
        div.innerHTML = `<div class="century-marker-text">${item.text}</div>`;
        return div;
    }
    
    renderBattleItem(battle, index) {
        const div = document.createElement('div');
        div.className = 'timeline-item';
        div.dataset.battleId = battle.id;
        
        // Add selected class if this is the selected battle
        if (this.selectedBattle && this.selectedBattle.id === battle.id) {
            div.classList.add('selected');
        }
        
        div.innerHTML = `
            <div class="timeline-item-dot"></div>
            <div class="timeline-item-content">
                <span class="timeline-item-name">${battle.name}</span>
                <span class="timeline-item-date">${battle.date.display}</span>
            </div>
        `;
        
        // Add click handler
        div.addEventListener('click', () => this.selectBattle(battle));
        
        return div;
    }
    
    selectBattle(battle) {
        this.selectedBattle = battle;
        
        // Update visual selection
        document.querySelectorAll('.timeline-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        const selectedElement = document.querySelector(`[data-battle-id="${battle.id}"]`);
        if (selectedElement) {
            selectedElement.classList.add('selected');
        }
        
        // Update content panel (placeholder for now)
        const contentPanel = document.querySelector('.content-placeholder');
        contentPanel.innerHTML = `
            <h2>${battle.name}</h2>
            <p>${battle.date.display}</p>
            <p><small>Details coming soon...</small></p>
        `;
    }
    
    initializeSearch() {
        const searchInput = document.getElementById('searchInput');
        let searchTimeout;
        
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.filterBattles(e.target.value);
            }, 300);
        });
    }
    
    filterBattles(searchTerm) {
        if (!searchTerm.trim()) {
            this.filteredBattles = [...this.battles];
        } else {
            const term = searchTerm.toLowerCase();
            this.filteredBattles = this.battles.filter(battle => 
                battle.name.toLowerCase().includes(term) ||
                battle.date.display.toLowerCase().includes(term)
            );
        }
        
        // Update timeline with filtered results
        const groupedItems = groupBattlesByCentury(this.filteredBattles);
        this.virtualScroller.updateItems(groupedItems);
        
        // Update count
        this.updateBattleCount();
    }
    
    initializeMinimap() {
        const minimap = document.getElementById('minimap');
        const viewport = document.getElementById('minimapViewport');
        const container = document.getElementById('timelineContainer');
        
        const updateMinimap = () => {
            if (container.scrollHeight <= container.clientHeight) {
                viewport.style.height = '100%';
                viewport.style.top = '0';
                return;
            }
            
            const scrollPercentage = container.scrollTop / (container.scrollHeight - container.clientHeight);
            const viewportHeight = (container.clientHeight / container.scrollHeight) * 100;
            
            viewport.style.height = `${Math.max(10, viewportHeight)}%`;
            viewport.style.top = `${scrollPercentage * (100 - viewportHeight)}%`;
        };
        
        // Update minimap on scroll
        container.addEventListener('scroll', updateMinimap);
        
        // Initial minimap update
        setTimeout(updateMinimap, 100);
        
        // Click on minimap to scroll
        minimap.addEventListener('click', (e) => {
            const rect = minimap.getBoundingClientRect();
            const clickY = e.clientY - rect.top;
            const clickPercentage = clickY / rect.height;
            
            const scrollTop = clickPercentage * (container.scrollHeight - container.clientHeight);
            container.scrollTop = scrollTop;
        });
    }
    
    updateBattleCount() {
        const countElement = document.getElementById('battleCount');
        countElement.textContent = `${this.filteredBattles.length} battles`;
    }
}

// Initialize timeline when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.timeline = new Timeline();
});