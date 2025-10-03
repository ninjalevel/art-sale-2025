document.addEventListener('DOMContentLoaded', () => {
    
    let allPaintings = [];
    let paintingsByCollection = {};
    
    // --- DOM Elements ---
    const gallery = document.getElementById('gallery');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = lightbox.querySelector('.lightbox-img');
    const lightboxTitle = lightbox.querySelector('.lightbox-title');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');

    let currentIndex = 0;

    // --- Fetch and Render ---
    async function loadSiteData() {
        try {
            const response = await fetch('site-data.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const siteData = await response.json();
            document.getElementById('artist_name').textContent = siteData.artist_name;
            const contactEmail = document.getElementById('contact_email');
            contactEmail.textContent = siteData.contact_email;
            contactEmail.parentElement.href = `mailto:${siteData.contact_email}`;
            document.getElementById('intro_title').textContent = siteData.intro_title;
            document.getElementById('intro_subtitle').textContent = siteData.intro_subtitle;

            // Event details
            document.getElementById('location').textContent = siteData.location;
            document.getElementById('date').textContent = siteData.date;
            document.getElementById('time').textContent = siteData.time;

            // Convert email in note to mailto link
            const noteElement = document.getElementById('note');
            const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi;
            const noteWithLink = siteData.note.replace(emailRegex, '<a href="mailto:$1">$1</a>');
            noteElement.innerHTML = noteWithLink;

            document.title = `${siteData.artist_name} - ${siteData.intro_subtitle}`
        } catch (error) {
            console.error("Could not load site data:", error);
        }
    }

    async function loadGalleryData() {
        try {
            await loadSiteData(); // Load site data first
            const response = await fetch('gallery-data.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            paintingsByCollection = await response.json();
            allPaintings = Object.values(paintingsByCollection).flatMap(collection => collection.paintings);
            populateGallery();
            setupEventListeners();
        } catch (error) {
            console.error("Could not load gallery data:", error);
            gallery.innerHTML = '<p class="error">Could not load gallery. Please try again later.</p>';
        }
    }




    // --- Populate Gallery ---
    function populateGallery() {
        gallery.innerHTML = ''; // Clear existing content
        Object.keys(paintingsByCollection).forEach(collectionName => {
            const collection = paintingsByCollection[collectionName];
            
            // Create a title for the collection
            const collectionTitle = document.createElement('h2');
            collectionTitle.className = 'collection-title';
            collectionTitle.textContent = collectionName;
            gallery.appendChild(collectionTitle);

            // Create a description for the collection
            if(collection.description) {
                const collectionDescription = document.createElement('p');
                collectionDescription.className = 'collection-description';
                collectionDescription.textContent = collection.description;
                gallery.appendChild(collectionDescription);
            }

            // Create a grid for the collection
            const collectionGrid = document.createElement('div');
            collectionGrid.className = 'gallery-grid';
            
            collection.paintings.forEach((p) => {
                const flatIndex = allPaintings.findIndex(painting => painting.file === p.file);
                const item = document.createElement('div');
                item.className = 'gallery-item';
                item.dataset.index = flatIndex;

                const img = document.createElement('img');
                img.src = `images/${p.file}`;
                img.alt = p.title;

                item.appendChild(img);
                collectionGrid.appendChild(item);
            });
            gallery.appendChild(collectionGrid);
        });
    }

    // --- Lightbox Logic ---
    function showLightbox(index) {
        currentIndex = index;
        const painting = allPaintings[currentIndex];

        lightboxImg.src = `images/${painting.file}`;
        lightboxTitle.textContent = painting.title;

        lightbox.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }

    function hideLightbox() {
        lightbox.classList.remove('show');
        document.body.style.overflow = 'auto';
    }

    function showNext() {
        currentIndex = (currentIndex + 1) % allPaintings.length;
        showLightbox(currentIndex);
    }

    function showPrev() {
        currentIndex = (currentIndex - 1 + allPaintings.length) % allPaintings.length;
        showLightbox(currentIndex);
    }

    // --- Event Listeners ---
    function setupEventListeners() {
        gallery.addEventListener('click', (e) => {
            const item = e.target.closest('.gallery-item');
            if (item) {
                showLightbox(parseInt(item.dataset.index));
            }
        });

        closeBtn.addEventListener('click', hideLightbox);
        nextBtn.addEventListener('click', showNext);
        prevBtn.addEventListener('click', showPrev);

        // Close lightbox on background click
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                hideLightbox();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (lightbox.classList.contains('show')) {
                if (e.key === 'ArrowRight') showNext();
                if (e.key === 'ArrowLeft') showPrev();
                if (e.key === 'Escape') hideLightbox();
            }
        });
    }

    // --- Initial Load ---
    loadGalleryData();
});