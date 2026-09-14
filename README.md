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

### Assignment 2

1. The new section (applying models): Education & Experience
When user opens/click the Education page, the request first goes through portofolio/urls.py, which connects it to main/urls.py. The /education/ route then calls show_education in views.py. This view retrieves data from the Education model and sends it to education.html through education_list. The template loops through the data (codes in education.html) and displays each object as a card, as seen in the education page. If there is no data, it displays an empty-state message. This whole process is also applied when user opens/click my Experience page. The difference is just the route and the html & lists.

2. If the Education & Experience data were written directly in the template, the HTML would become packed with both code & content, hence become harder to read. By using model, the data is stored seperately in the database while the HTML only manages how it is displayed. Of course, using models would make the maintenance become easier as it ables to add or update records through the Django shell without rewriting the card structure. For example is when I want to change the description of my education card, I just need to run the command Education.objects.filter(...).update(...)

3. In simple words, makemigrations creates instructions based on changes in the models, while migrate applies those changes to the database. For example in this project is when I added stage_choices and stage for my experience model and skills for my education model. Then for us to be able to insert our data to the database, we are required to run the command makemigrations and migrate beforehand. Otherwise, Django would return an error because the database columns did not exist yet.

WORKING STRATEGY
1. Work on the Education page
    - Move education page from the profile page into its own page
    - Change the layout from side-by-side to vertically stacked landscape cards 
    - Turn skills list into chip
    - Add links (buttons) that directs to experience section
2. Work on the Experience page
    - Seperate University and High School section experiences
    - Add organizations and committee into categories
    - Add experiences through Django shell
3. I used Codex AI mainly to understand & asked for the confirmation of the MVT flow, models, migrations, diagnose errors, get suggestion for the CSS layout & styles, and the unit tests making. I reviewed the suggestions and implemented the changes the AI suggest manually based on my own portfolio design.