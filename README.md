Name: Alyssa Rahma Adjani

NPM: 2506558466

Class: PBP KKI

latihan-branch

### Assignment 1

1. Yes, I used two of the HTML5 semantics mentioned. In the Tutorial 1, I used <section> for the hero/about me section. For Assignment 1, not only did I use <section>, but I also used the <article> semantic for my education background cards in the new section. So far, wrapping my education cards in <article> tags made it so much easier for me to understand the structure of my work. 
Moreover, it has also greatly affected the CSS styling process in a positive way. Since, the content of both cards represents independent educational milestones, using <article> allowed me to easily target specific sections in CSS (such as custom illustrations) and card copy.

2. The main layout challenge I encountered was adjusting my two education cards from a horizontal layout on desktop view to a vertical stacked layout for mobile view. I solved this by utilizing a media query @media (max-wdith: 600px) to change the CSS Grid grid-template-columns property from two equal columns (repeat(2, minmax(0, 1fr))) to a single column (1fr).
Additionally, when dealing with PNG or SVG (for decorations), I was hoping they would adapt automatically, but on mobile view, I realized everything was cramped. This was the moment I learned something new while fixing it: position:, right:, top:, overflow:, and last but not least,  z-index. Those properties helped me to adjust the attached image in the place I expected to be. 

3. I feel like my vision for my portfolio design leans toward a playful & colorful aesthetic. Hence, it is somewhat difficult seeing it remain entirely static and still on the screen. I would say the limitation is the lack of interactive motion or elements, as I did not explore much there. For future iterations, I wish to add bouncy hover states or Interactive card tilts for my education cards improvements, and simple but fun animations. 

WORKING STRATEGY:
1. Building website prototype and design using Figma. Plugin used:
    - html.to.design--by<div>RIOTS
2. Analyze & convert designs made to HTML+CSS code using Figma. Plugin used:
    - Anima
3. Use CHATGPT & Gemini AI assistance to adjust my code and the code taken from Anima (to execute expected design). Focused parts that needs assistance:
    - Layout architecture for my education cards
    - Placement & layering for my background vectors
    - Responsive breakpoints & layout shifts (half Me half AI)
    - Asked AI about the design like is it executable, is it responsive when implemented, etc.