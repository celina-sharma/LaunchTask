
        const accordionItems = document.querySelectorAll('.accordion-item');

        const closeAllItems = () => {
            accordionItems.forEach(item => {
                item.classList.remove('active');
                item.querySelector('.accordion-icon').textContent = '+';
            });
        };

        if (accordionItems.length > 1) {
            accordionItems[1].classList.add('active');
            accordionItems[1].querySelector('.accordion-icon').textContent = '−';
        }

        accordionItems.forEach(item => {
            const header = item.querySelector('.accordion-header');
            const icon = item.querySelector('.accordion-icon');

            header.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                closeAllItems();

                if (!isActive) {
                    item.classList.add('active');
                    icon.textContent = '−';
                }
            });
        });
   