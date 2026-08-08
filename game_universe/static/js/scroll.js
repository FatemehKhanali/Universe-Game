const scrollContainer = document.getElementById('gameScroll');


document.getElementById('scrollLeftBtn').addEventListener('click', () => {
  scrollContainer.scrollBy({ left: -300, behavior: 'smooth' });
});


document.getElementById('scrollRightBtn').addEventListener('click', () => {
  scrollContainer.scrollBy({ left: 300, behavior: 'smooth' });
});


let scrollAmount = 0;
const scrollStep = 300; 
const scrollDelay = 3000; 

setInterval(() => {
  
  if (scrollContainer.scrollLeft + scrollContainer.offsetWidth >= scrollContainer.scrollWidth) {
    scrollAmount = 0;
    scrollContainer.scrollTo({ left: 0, behavior: 'smooth' });
  } else {
    scrollAmount += scrollStep;
    scrollContainer.scrollBy({ left: scrollStep, behavior: 'smooth' });
  }
}, scrollDelay);


