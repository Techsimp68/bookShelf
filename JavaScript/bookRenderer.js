document.addEventListener('DOMContentLoaded', async () => {
  const mode = localStorage.getItem('storyMode'); // 'classic' or 'dynamic'
  const chapterText = document.getElementById('chapter-text');
  const choiceContainer = document.getElementById('choice-container');
  const nextBtn = document.getElementById('next-chapter');

  let currentChapter = 1;
  let storyPath = []; // for dynamic branching

  async function fetchChapter(chapterNum, path = []) {
    const response = await fetch(`/get_chapter?chapter=${chapterNum}&path=${path.join(',')}`);
    const data = await response.json();
    return data;
  }

  async function renderChapter() {
    const data = await fetchChapter(currentChapter, storyPath);
    chapterText.textContent = data.content;

    // Handle choices if dynamic mode
    if (mode === 'dynamic' && data.choices) {
      choiceContainer.innerHTML = ''; // clear old choices
      choiceContainer.style.display = 'block';

      data.choices.forEach((choice, index) => {
        const btn = document.createElement('button');
        btn.textContent = choice.label;
        btn.onclick = () => {
          storyPath.push(index);       // save user choice path
          currentChapter++;
          renderChapter();             // load next chapter based on path
        };
        choiceContainer.appendChild(btn);
      });

      nextBtn.style.display = 'none'; // hide next button if dynamic
    } else {
      choiceContainer.style.display = 'none';
      nextBtn.style.display = 'inline';
    }
  }

  nextBtn.addEventListener('click', () => {
    currentChapter++;
    renderChapter();
  });

  renderChapter(); // Load the first chapter
});
