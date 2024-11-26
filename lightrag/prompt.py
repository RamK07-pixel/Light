GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["Question Number","Score", "Question", "Topic", "Common Misconceptions","Subject","Explanation"]

PROMPTS["entity_extraction"] = """-Goal-
Given a JEE Mains exam-related text document and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalize the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and relevance
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level keywords that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level keywords as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in English as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
Example 1:

Entity_types: [performance, question, topic, common misconceptions, explanation]
Text:
this student data struggled with questions related to thermodynamics, particularly in concepts involving entropy. His performance in this topic showed a consistent pattern of misunderstanding how entropy changes in isolated systems, despite attempts to grasp the formulaic applications. A common misconception among students here is that entropy always decreases, which leads to errors in analyzing irreversible processes.

However, the explanation in the question review emphasized that entropy in isolated systems always increases for irreversible processes, clearing up the misconception. Other topics like Kinematics saw him excel, demonstrating his ability to solve motion problems with ease.

################
Output:
("entity"{tuple_delimiter}"he"{tuple_delimiter}"student"{tuple_delimiter}"he is a student attempting JEE Mains questions, showing strengths in kinematics but struggling with thermodynamics."){record_delimiter}
("entity"{tuple_delimiter}"Thermodynamics"{tuple_delimiter}"topic"{tuple_delimiter}"Thermodynamics is a subject area where he faced challenges, particularly with the concept of entropy."){record_delimiter}
("entity"{tuple_delimiter}"Entropy Changes in Isolated Systems"{tuple_delimiter}"common misconceptions"{tuple_delimiter}"A common misconception is that entropy always decreases, causing errors in analysis of irreversible processes."){record_delimiter}
("entity"{tuple_delimiter}"Entropy and Irreversible Processes"{tuple_delimiter}"explanation"{tuple_delimiter}"Entropy in isolated systems always increases for irreversible processes, clearing up the misconception."){record_delimiter}
("entity"{tuple_delimiter}"Kinematics"{tuple_delimiter}"topic"{tuple_delimiter}"Kinematics is an area where he excelled, solving motion problems with ease."){record_delimiter}
("relationship"{tuple_delimiter}"he"{tuple_delimiter}"Thermodynamics"{tuple_delimiter}"he struggled with thermodynamics, particularly entropy-related concepts."{tuple_delimiter}"topic difficulty, performance analysis"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Thermodynamics"{tuple_delimiter}"Entropy Changes in Isolated Systems"{tuple_delimiter}"Thermodynamics includes the misconception about entropy always decreasing."{tuple_delimiter}"misconception linkage, conceptual clarity"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Entropy Changes in Isolated Systems"{tuple_delimiter}"Entropy and Irreversible Processes"{tuple_delimiter}"The misconception about entropy decreasing is corrected by the explanation about entropy increases in irreversible processes."{tuple_delimiter}"conceptual resolution, understanding"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"he"{tuple_delimiter}"Kinematics"{tuple_delimiter}"he excelled in solving kinematics problems, showcasing strong understanding of motion."{tuple_delimiter}"performance highlight, strength identification"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"thermodynamics, kinematics, entropy, JEE Mains, student performance"){completion_delimiter}
#############################
Example 2:

Entity_types: [student, performance, question, topic, common misconceptions, explanation]
Text:
this data performance in the Mechanics section of the JEE Mains test showcased a strong understanding of Newtonian principles but was marked by errors in understanding relative motion. The most frequent issue was applying incorrect frames of reference. This common misconception, shared by many students, is addressed by clarifying the importance of consistent reference frames when analyzing motion.

################
Output:
("entity"{tuple_delimiter}"she"{tuple_delimiter}"student"{tuple_delimiter}"she is a student performing well in mechanics, with errors in understanding relative motion."){record_delimiter}
("entity"{tuple_delimiter}"Mechanics"{tuple_delimiter}"topic"{tuple_delimiter}"Mechanics is a section where she demonstrated strong Newtonian principles but struggled with relative motion."){record_delimiter}
("entity"{tuple_delimiter}"Relative Motion"{tuple_delimiter}"common misconceptions"{tuple_delimiter}"A common misconception is the incorrect application of frames of reference in relative motion."){record_delimiter}
("entity"{tuple_delimiter}"Frames of Reference in Relative Motion"{tuple_delimiter}"explanation"{tuple_delimiter}"Consistent reference frames are crucial for analyzing motion correctly."){record_delimiter}
("relationship"{tuple_delimiter}"she"{tuple_delimiter}"Mechanics"{tuple_delimiter}"she excelled in mechanics but made errors in relative motion, particularly in using reference frames."{tuple_delimiter}"performance variation, concept struggle"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Relative Motion"{tuple_delimiter}"Frames of Reference in Relative Motion"{tuple_delimiter}"The misconception about relative motion is resolved by the explanation on the importance of consistent frames of reference."{tuple_delimiter}"conceptual resolution, mechanics clarity"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"mechanics, Newtonian principles, relative motion, frames of reference, JEE Mains"){completion_delimiter}
#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""
PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we have full context.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[ 
    "entiti_continue_extraction" 
] = """MANY entities were missed in the last extraction. Add them below using the same format:
"""

PROMPTS[ 
    "entiti_if_loop_extraction" 
] = """It appears some entities may have still been missed. Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.

---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
Example 1:

Query: "How is the Performance in Mathematics?"
################
Output:
{{
  "high_level_keywords": ["Mathematics", "Performance", "Algebra", "Quadratic equations", "Polynomials", "Factoring", "Simplifying expressions", "Roots", "Equation solving"],
  "low_level_keywords": ["Factoring", "Completing the square", "Quadratic formula", "Roots of the equation", "Polynomial long division", "Misunderstanding signs", "Common factoring errors", "Variable isolation"]
}}
#############################
Example 2:

Query: "What are the key topics in Physics?"
################
Output:
{{
  "high_level_keywords": ["Physics", "Key topics", "Physics concepts"],
  "low_level_keywords": ["Mechanics", "Electromagnetism", "Quantum physics", "Relativity", "Thermodynamics", "Forces", "Motion", "Energy"]
}}
#############################
Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Chemistry", "Molar mass", "Chemical formula", "Molecular weight", "Sulfuric acid"],
  "low_level_keywords": ["H2SO4", "Sulfur", "Oxygen", "Hydrogen", "Atomic masses", "Periodic table", "Chemical reaction"]
}}
#############################
Example 4:

Query: "How is the performance of students in understanding the concept of molar mass in Chemistry? What are the low-scoring areas related to the calculation of molar mass?"
################
Output:
{{
  "high_level_keywords": ["Chemistry", "Performance", "Understanding", "Molar mass", "Student evaluation", "Low-scoring areas", "Calculation", "Concept understanding"],
  "low_level_keywords": ["Molar mass", "Periodic table", "Atomic mass", "Chemical formula", "Sulfuric acid", "Hydrogen", "Oxygen", "Errors in calculation", "Student mistakes"]
}}
#############################
Example 5:

Query: "What is the general performance in Kinematics? Can you identify the common misconceptions or low-scoring areas related to acceleration and motion equations?"
################
Output:
{{
  "high_level_keywords": ["Physics", "Performance", "Kinematics", "Acceleration", "Motion equations", "Common misconceptions", "Student performance"],
  "low_level_keywords": ["Acceleration", "Velocity", "Position equation", "Derivative", "Time", "Misunderstanding acceleration", "Calculations errors", "Units of measurement", "t^2 term"]
}}
#############################
Example 6:

Query: "How are students performing in solving linear equations? Are there any specific low-scoring areas related to isolating variables or dealing with constants?"
################
Output:
{{
  "high_level_keywords": ["Mathematics", "Performance", "Linear equations", "Solving for x", "Isolating variables", "Constants", "Low-scoring areas", "Student evaluation"],
  "low_level_keywords": ["Linear equation", "Variable isolation", "x", "Constants", "Addition", "Subtraction", "Missteps in algebraic manipulation", "Basic arithmetic errors"]
}}
#############################
Example 7:

Query: "How are students performing in Algebra, particularly in solving quadratic equations and working with polynomials? What are the common low-scoring areas related to factoring, simplifying expressions, and solving for roots?"
################
Output:
{{
  "subject": "Mathematics",
  "high_level_keywords": ["Mathematics", "Performance", "Algebra", "Quadratic equations", "Polynomials", "Factoring", "Simplifying expressions", "Roots", "Equation solving"],
  "low_level_keywords": ["Factoring", "Completing the square", "Quadratic formula", "Roots of the equation", "Polynomial long division", "Misunderstanding signs", "Common factoring errors", "Variable isolation"]
}}
#############################
Example 8:

Query: "How are students performing in Mechanics, specifically in understanding force and motion? Can you identify the low-scoring areas related to Newton’s Laws of Motion and calculations of velocity and acceleration?"
################
Output:
{{
  "subject": "Physics",
  "high_level_keywords": ["Physics", "Performance", "Mechanics", "Force", "Motion", "Newton's Laws", "Velocity", "Acceleration", "Calculations", "Understanding concepts"],
  "low_level_keywords": ["First law", "Second law", "Third law", "Friction", "Mass", "Velocity calculation", "Acceleration calculation", "Force diagrams", "Vector addition", "Common formula errors"]
}}
#############################
Example 9:

Query: "How is the performance of students in understanding the concept of the periodic table and atomic structure in Chemistry? What are the low-scoring areas related to identifying elements, groups, and periods?"
################
Output:
{{
  "subject": "Chemistry",
  "high_level_keywords": ["Chemistry", "Performance", "Periodic table", "Atomic structure", "Groups", "Periods", "Elements", "Concept understanding"],
  "low_level_keywords": ["Atomic number", "Electron configuration", "Valence electrons", "Groups", "Periods", "Element identification", "Misunderstanding periodic trends", "Family properties", "Isotopes"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:
"""

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.

---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""
