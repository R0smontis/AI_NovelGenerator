# prompt_definitions_en.py
# -*- coding: utf-8 -*-
"""
Centralized storage for all prompts.
Modified version: Removed forced narrative frameworks (Snowflake Method, Character Arc, Three-Act Suspense).
User guidance (user_guidance) is the highest priority — don't add content the user didn't request.
"""

# =============== Draft Generation: Current Chapter Summary & Knowledge Base ===============
summarize_recent_chapters_prompt = """\
As a professional novel editor, you are generating a precise summary of the current chapter based on the completed content of the previous three chapters and the current chapter's information.

Previous three chapters content:
{combined_text}

Current chapter information:
Chapter {novel_number} "{chapter_title}":
├── Chapter role: {chapter_role}
├── Core function: {chapter_purpose}
├── Chapter summary: {chapter_summary}

Next chapter information:
Chapter {next_chapter_number} "{next_chapter_title}":
├── Chapter role: {next_chapter_role}
├── Core function: {next_chapter_purpose}
├── Chapter summary: {next_chapter_summary}

**Summary Rules**:
1. Objectively record what happened; avoid subjective interpretation
2. Focus on plot progression and character development
3. If user guidance specifies priorities for this chapter, center the summary around it
4. User guidance: {user_guidance}

Now write a concise "Current Chapter Summary" in at most 800 words.

Output format (no additional explanation):
Current Chapter Summary: <write the summary here>
"""

# Knowledge base search query prompt (kept as-is, functional)
knowledge_search_prompt = """\
Based on the following current writing requirements, generate appropriate knowledge base search keywords:

Chapter metadata:
- Preparing to write: Chapter {chapter_number}
- Chapter theme: {chapter_title}
- Core characters: {characters_involved}
- Key items: {key_items}
- Scene location: {scene_location}

Writing goals:
- Chapter role: {chapter_role}
- Core function: {chapter_purpose}

Current summary:
{short_summary}

- User guidance:
{user_guidance}

- Core characters (may not be specified): {characters_involved}
- Key items (may not be specified): {key_items}
- Spatial coordinates (may not be specified): {scene_location}
- Time pressure (may not be specified): {time_constraint}

Generation rules:
1. Keyword combination logic:
   - Type 1: [entity] + [attribute] (e.g., "quantum computer malfunction log")
   - Type 2: [event] + [consequence] (e.g., "laboratory explosion radiation leak")
   - Type 3: [location] + [feature] (e.g., "underground city oxygen circulation system")
2. Priority:
   - First choice: terms explicitly mentioned in user guidance
   - Second choice: core items/locations involved in the current chapter
   - Last: supplementary extended concepts that may be relevant
3. Filter mechanism:
   - Exclude concepts with an abstraction level too high
   - Exclude vocabulary with over 60% repetition rate from the previous 3 chapters

Generate 3-5 sets of search terms, listed in descending order of priority.
Format: connect 2-3 keywords per set with "·", one set per line

Example:
tech company · data breach
underground lab · genetic engineering · forbidden experiment
"""

# Knowledge base content filter prompt (kept as-is, functional)
knowledge_filter_prompt = """\
Filter the knowledge base content:

Content to be filtered:
{retrieved_texts}

Current narrative requirements:
{chapter_info}

Filtering process:

1. Conflict detection:
   - Delete content with over 40% repetition rate compared to existing summaries
   - Mark content with setting contradictions (use ▲ prefix)

2. Value assessment:
   - Key value points (marked with ❗):
     · Provides new possibilities for character relationships
     · Contains adaptable writing material
     · Has at least 2 extensible detail anchor points
   - Secondary value points (marked with ·):
     · Supplements environmental details
     · Provides technical/procedural descriptions

3. Structural reorganization:
   - Classify by "plot material / character dimension / world details / writing technique"
   - Add applicable scene hints to each category

Output format:
[Category name] -> [Applicable scene]
❗/· [Content snippet] (▲ conflict note)
...

Output the final text only, do not explain anything.
"""

# =============== 1. Core Seed ===================
core_seed_prompt = """\
Based on the user's input, summarize the core of the story in one sentence:

User guidance: {user_guidance}
Genre: {genre}
Length: approximately {number_of_chapters} chapters (each chapter {word_number} words)

Requirements:
1. Faithfully reflect the user's guidance; do not add conflicts or crises the user didn't mention
2. If the user has already provided a clear story summary, refine upon it directly
3. Express precisely in 25-100 words

Return only the story core text, do not explain anything.
"""

# =============== 2. Character Design ===================
character_dynamics_prompt = """\
Based on the following elements:
- User guidance: {user_guidance}
- Core seed: {core_seed}

Design the core characters for the story. For each character, include:
- Basic info: background, appearance, gender, age, occupation, etc.
- Personality traits and behavioral patterns
- Role and general direction in the story

Requirements:
1. Prioritize extracting existing character info from user guidance
2. If user guidance already has detailed character settings, follow them faithfully
3. For dimensions the user didn't specify, fill in with reasonable but restrained inference
4. Do not force every character to have "dark secrets" or "hidden depths"

Output the final text only, do not explain anything.
"""

# =============== 3. World / Background Setting ===================
world_building_prompt = """\
Based on the following elements:
- User guidance: {user_guidance}
- Core seed: "{core_seed}"

Build the story's background setting based on what the user's guidance actually involves.

Key principles:
- If user guidance already describes the world, follow it faithfully with only reasonable supplementation
- If user guidance mentions no worldbuilding at all (e.g., realistic fiction, daily life), simply describe the era/region/social context briefly
- Do not force a grand multi-dimensional worldbuilding system the user never asked for

Output the final text only, do not explain anything.
"""

# =============== 4. Plot Architecture ===================
plot_architecture_prompt = """\
Based on the following elements:
- User guidance: {user_guidance}
- Core seed: {core_seed}
- Character system: {character_dynamics}
- Worldbuilding: {world_building}

Design the overall plot architecture following the user's guidance.

Key principles:
1. Faithfully follow the story direction in user guidance; don't add major twists the user didn't mention
2. If user guidance already has a detailed outline, refine upon it — don't rewrite
3. Follow the story's natural pacing; don't force a specific narrative formula
4. Total chapters: approximately {number_of_chapters}; distribute pacing reasonably

Output the final text only, do not explain anything.
"""

# =============== 5. Chapter Outline Generation ===================
chapter_blueprint_prompt = """\
Based on the following elements:
- User guidance: {user_guidance}
- Novel architecture:
{novel_architecture}

Design a chapter outline for {number_of_chapters} chapters. Each chapter must specify:
- Chapter title
- Chapter role (character/event/transition, etc.)
- Core content (what happens in this chapter)
- Chapter summary (one-sentence overview)

Output format example:
Chapter n - [Title]
Chapter role: [character/event/transition/...]
Core content: [main plot or character development]
Chapter summary: [one-sentence overview]

Chapter n+1 - [Title]
Chapter role: [character/event/transition/...]
Core content: [main plot or character development]
Chapter summary: [one-sentence overview]

Requirements:
- Use concise language; keep each chapter description under 100 words
- Be faithful to the story direction in user guidance
- Do not include a concluding chapter before all {number_of_chapters} chapters have been generated
- If user guidance already provides a complete chapter outline, follow it faithfully

Output the final text only, do not explain anything.
"""

chunked_chapter_blueprint_prompt = """\
Based on the following elements:
- User guidance: {user_guidance}
- Novel architecture:
{novel_architecture}

The total outline to be generated is {number_of_chapters} chapters.

Existing chapter list (if empty, this is the initial generation):

{chapter_list}

Now design the outline for Chapters {n} through {m}. Each chapter must specify:
- Chapter title
- Chapter role (character/event/transition, etc.)
- Core content (what happens in this chapter)
- Chapter summary (one-sentence overview)

Output format example:
Chapter n - [Title]
Chapter role: [character/event/transition/...]
Core content: [main plot or character development]
Chapter summary: [one-sentence overview]

Chapter n+1 - [Title]
Chapter role: [character/event/transition/...]
Core content: [main plot or character development]
Chapter summary: [one-sentence overview]

Requirements:
- Use concise language; keep each chapter description under 100 words
- Be faithful to the story direction in user guidance
- Do not include a concluding chapter before all {number_of_chapters} chapters have been generated
- If user guidance already provides a complete chapter outline, follow it faithfully

Output the final text only, do not explain anything.
"""

# =============== 6. Previous Text Summary Update ===================
summary_prompt = """\
The following is the newly completed chapter text:
{chapter_text}

This is the current previous-text summary (may be empty):
{global_summary}

Please update the previous-text summary based on the new content from this chapter.
Requirements:
- Retain existing important information while incorporating new plot key points
- Describe the overall progress of the book in concise, coherent language
- Describe objectively; do not speculate or elaborate
- Keep the total word count within 2000 words

Return only the previous-text summary text, do not explain anything.
"""

# =============== 7. Character State Update ===================
create_character_state_prompt = """\
Based on the current character setting: {character_dynamics}

Please generate a character state document in the following format:
Example:
Zhang San:
├── Items:
│  ├── Blue robe: a worn cyan long robe stained with dark red marks
│  └── Cold iron longsword: a broken iron sword with ancient runes carved on the blade
├── Abilities
│  ├── Skill 1 - Strong mental perception: able to sense the thoughts of people nearby
│  └── Skill 2 - Invisible attack: can release a mental attack that cannot be seen with the naked eye
├── Status
│  ├── Physical status: tall and upright, wearing ornate armor, with a cold expression
│  └── Mental status: currently calm, but harboring hidden ambitions and unease over control of Liuxi Village
├── Main character relationship network
│  ├── Li Si: Zhang San has been connected to her since childhood and has always kept watch over her growth
│  └── Wang Er: the two share a complicated past; a recent conflict has made the other feel threatened
├── Triggered or deepened events
│  ├── Unknown symbols suddenly appear in the village: these symbols seem to hint that a major event is about to occur in Liuxi Village
│  └── Li Si is pierced through the skin: this event made both realize the other's formidable strength, prompting them to quickly leave the group

Character name:
├── Items:
│  ├── Some item (prop): description
│  └── XX longsword (weapon): description
│   ...
├── Abilities
│  ├── Skill 1: description
│  └── Skill 2: description
│   ...
├── Status
│  ├── Physical status:
│  └── Mental status: description

├── Main character relationship network
│  ├── Li Si: description
│  └── Wang Er: description
│   ...
├── Triggered or deepened events
│  ├── Event 1: description
│  └── Event 2: description
    ...

New characters:
- (Fill in basic information for any new or temporarily appearing characters here)

Requirements:
Return only the written character state text, do not explain anything.
"""

update_character_state_prompt = """\
The following is the newly completed chapter text:
{chapter_text}

This is the current character state document:
{old_state}

Please update the main character states in the following format:
Example:
Zhang San:
├── Items:
│  ├── Blue robe: a worn cyan long robe stained with dark red marks
│  └── Cold iron longsword: a broken iron sword with ancient runes carved on the blade
├── Abilities
│  ├── Skill 1 - Strong mental perception: able to sense the thoughts of people nearby
│  └── Skill 2 - Invisible attack: can release a mental attack that cannot be seen with the naked eye
├── Status
│  ├── Physical status: tall and upright, wearing ornate armor, with a cold expression
│  └── Mental status: currently calm, but harboring hidden ambitions and unease over control of Liuxi Village
├── Main character relationship network
│  ├── Li Si: Zhang San has been connected to her since childhood and has always kept watch over her growth
│  └── Wang Er: the two share a complicated past; a recent conflict has made the other feel threatened
├── Triggered or deepened events
│  ├── Unknown symbols suddenly appear in the village: these symbols seem to hint that a major event is about to occur in Liuxi Village
│  └── Li Si is pierced through the skin: this event made both realize the other's formidable strength, prompting them to quickly leave the group

Character name:
├── Items:
│  ├── Some item (prop): description
│  └── XX longsword (weapon): description
│   ...
├── Abilities
│  ├── Skill 1: description
│  └── Skill 2: description
│   ...
├── Status
│  ├── Physical status:
│  └── Mental status: description

├── Main character relationship network
│  ├── Li Si: description
│  └── Wang Er: description
│   ...
├── Triggered or deepened events
│  ├── Event 1: description
│  └── Event 2: description
    ...

......

New characters:
- Basic information for any new or temporarily appearing characters; keep it brief, do not expand. Characters who have faded from the story may be removed.

Requirements:
- Make additions and deletions directly on the existing document
- Do not change the original structure; keep the language concise and organized

Return only the updated character state text, do not explain anything.
"""

# =============== 8. Chapter Body Writing ===================

# 8.1 First chapter draft prompt
first_chapter_draft_prompt = """\
Preparing to write: Chapter {novel_number} "{chapter_title}"
Chapter role: {chapter_role}
Core content: {chapter_purpose}
Chapter summary: {chapter_summary}

Available elements:
- Core characters (may not be specified): {characters_involved}
- Key items (may not be specified): {key_items}
- Spatial coordinates (may not be specified): {scene_location}
- Time pressure (may not be specified): {time_constraint}

Reference documents:
- Novel settings:
{novel_setting}

User guidance (HIGHEST PRIORITY):
{user_guidance}

Complete the body of Chapter {novel_number}, with a word count requirement of {word_number} words.

Writing principles (in priority order):
1. User guidance is the highest priority — write what the user asked for; don't add what they didn't request
2. Follow the chapter summary and core content faithfully
3. If user guidance specifies specific scenes, dialogue, or plot, use them first
4. Write naturally; don't artificially create dramatic conflict or suspense

Format requirements:
- Return only the chapter body text
- Do not use sub-chapter headings
- Do not use markdown formatting
"""

# 8.2 Subsequent chapter draft prompt
next_chapter_draft_prompt = """\
Reference documents:
└── Previous text summary:
    {global_summary}

└── Previous chapter closing paragraph:
    {previous_chapter_excerpt}

└── User guidance (HIGHEST PRIORITY):
    {user_guidance}

└── Character states:
    {character_state}

└── Current chapter summary:
    {short_summary}

Current chapter information:
Chapter {novel_number} "{chapter_title}":
├── Chapter role: {chapter_role}
├── Core content: {chapter_purpose}
├── Chapter summary: {chapter_summary}
├── Word count requirement: {word_number} words
├── Core characters: {characters_involved}
├── Key items: {key_items}
├── Scene location: {scene_location}
├── Time pressure: {time_constraint}

Next chapter outline
Chapter {next_chapter_number} "{next_chapter_title}":
├── Chapter role: {next_chapter_role}
├── Core content: {next_chapter_purpose}
├── Chapter summary: {next_chapter_summary}

Knowledge base reference: (apply by priority)
{filtered_context}

Knowledge base rules:
- Writing techniques can be referenced, but don't change content just to use them
- Setting materials: only use within the scope of user guidance or established worldbuilding
- Do not directly copy plot patterns from existing chapters
- If knowledge base content conflicts with user guidance, user guidance takes precedence

Based on all the above, complete the body of Chapter {novel_number}, with a word count requirement of {word_number} words.

Writing principles (in priority order):
1. User guidance is the highest priority — faithfully follow the user's requirements and outline
2. Connect naturally with the previous text summary and previous chapter's closing paragraph
3. Maintain continuity with the next chapter outline
4. Do not add major plot twists or worldbuilding elements that the user didn't mention

Format requirements:
- Return only the chapter body text
- Do not use sub-chapter headings
- Do not use markdown formatting
"""

Character_Import_Prompt = """\
Based on the following text content, analyze all characters and their attribute information. Strictly follow the format requirements below:

<<Character State Format Requirements>>
1. Must include the following five categories (in order):
   ● Items ● Abilities ● Status ● Main character relationship network ● Triggered or deepened events
2. Each attribute entry must use the format [name: description]
   Example: ├──Blue robe: a worn cyan long robe stained with dark red marks
3. Status must include:
   ● Physical status: [current physical condition]
   ● Mental status: [current mental/psychological condition]
4. Relationship network format:
   ● [Character name]: [relationship type, e.g., "rival" / "ally"]
5. Triggered event format:
   ● [Event name]: [brief description and impact]

<<Example>>
Elder Li:
├── Items:
│  ├── Blue robe: a worn cyan long robe stained with dark red marks
│  └── Cold iron longsword: the blade is cracked, with "Azure Cloud" runes engraved on it
├── Abilities:
│  ├── Mental perception: can sense living beings within a 30-meter radius
│  └── Sword-qi suppression: releases mental pressure through eye contact
├── Status:
│  ├── Physical status: right arm has an unhealed sword wound
│  └── Mental status: feels wary of Su Mingyuan's strength
├── Main character relationship network:
│  ├── Su Mingyuan: rival, former colleague from ten years ago
│  └── Lin Wan'er: a secretly cultivated successor
├── Triggered or deepened events:
│  ├── Armory raid: lost three heirloom swords, affecting combat strength
│  └── Anonymous threatening letter: the paper smells of sandalwood, hinting at an internal leak

Please strictly analyze the following content in the above format:
<<Start of novel text to be analyzed>>
{content}
<<End of novel text to be analyzed>>
"""

enrich_prompt = """\
The following chapter text is short. Please expand it while maintaining plot continuity to make it more substantial, aiming for approximately {word_number} words. Output only the final text, do not explain anything.
Original content:
{chapter_text}
"""
