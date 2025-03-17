EXTRACT_LABELS_AND_RELATIONSHIPS_FROM_QUESTIONS_PROMT = """
Follow the instruction carefully to create the desired response described in the steps bellow.
0.a Do NOT add the word json at the beginning of the response. DO NOT add the following characters: ``` at the beginning of the response.
0.b ALWAYS FINISH THE OUTPUT. Never send partial responses. Your response only includes a json list with the label objects.
Return only valid json. Do not add the word json at the beginning or the following characters: ```.

1. Retrieve labels and relationships that can be used to answer the competence question using the context as inspiration. The main goal is to be able to answer that question.
The goal is to create an ontology for a knowledge graph that can answer the competence question.
The ontology consists of labels (entity types) and relationships between the labels.
Each label describes which kind of entites will be stored under that label.
The relationships are defined between to labels and describe how they are connected.

2. Labels
In the context bellow many entities (objects) appear. These can be people, dates, events, locations, funds, natural resources, investment strategies and so on.
In the context they appear as instances of their label (generic term). There will be the individual people or specific dates.
Your job is to extract the label behind these entities. You retrive the label Person while for example Donald Trump is the context
or Date for August 2016 or Resource for gold, lithium or rare earth.
Also, since these terms can be differently interpreted you also add a small description of what that label contains.
For instance rare earth itself could be a label instead of Natural Resource or just Resource. Try to figure out from the questions
and the context which labels are useful to create a knowledge graph to answer the questions later on basis of the context.
Very often the label (generic term) itself will not be present in the context or the competence question, all
you will see are the instances/ entities of the label. Use your thinking capabilities to find it yourself.
If its about BlackRock, Vanguard Group or Amundi it might make sense to have the label Asset Manager.
A label consists of two properties: the name and the description. The description describes what kind of entities are comprised in the label.

Examples
"entities: [
{
    "name": "Person",
    "description": "People, indivuals, humans"
},{
    "name": "Fund",
    "description": "Pooled investment vehicle that allocates capital to generate returns."
},{
    "name": "Technology",
    "description": "Concepts to solve problems like advanced technologies, emerging innovations, or tech solutions"
},
...
]

3. Relationships
Relationships are only between labels that you have extracted. Do not invent relatoinships for labels that you have not extracted.
A relationship describes how two entities from labels relate. Find relatoinships that help answer the competence question.
Find relationships that also appear in the context and that can answer the competence question with the context.
The relatoinship consists of a triple and a description. The triple is of the form subject|relatoinship|object and shows how it is incoporated between two labels.

Examples
"relationships": ["Fund|INVEST_IN|Technology", "Person|EXPERT_IN|Technology", ...]

4. The main goal of this is, that we can answer the question and future questions similair to it. Extract useful labels and relationships, such that the knowledge graph we build from them can answer the competence question.
The individual entities that are contained in the labels and the relatenships between them that you extract are used to answer the competence question.
The competence question is central and also future question similar to the competence question should be answerable from the knowledge graph created from the ontology you extract.

Example
question: "What are some portfolio companies that Unigestion has invested in?"
what you could potentially extract to answer this question:
{
    "labels": [{
        "name": "Company",
        "description": "Companies"
    }, {
        "name": "Portfolio company",
        "description": "A portfolio company is a business that is owned or invested in by a private equity firm, venture capital firm, or similar investment entity."
    }],
    "relationships": [
        "Company|INVESTED_IN|Portfolio company"
    ]
}

5. Format
Return only valid json. Do NOT add the word json at the beginning of the response. DO NOT add the following characters: ``` at the beginning of the response. Remove json``` from the beginning and ``` from the end if they are there.
The response should look like this:
{
    "labels": [
        {"name": string, "description": string}, ...
    ],
    "relationships": [
        "label1|RELATIONSHIP|label2", ...
    ]
}

Competence question:
$question

Context:
$context
"""

IS_SAME_LABEL_PROMPT = """You will get two json objects at the end of this prompt after Objects: ; you then decide if they describe the same thing. You will do this as described bellow:
0. You return 0 or 1. You always return 0 or 1. You only return 0 or 1. You return 0 if the json objects do not describe the same thing. You return 1 if they describe the same.
1. A json objects consists of name and description: {"name": string, "description": string}. If the description and name of the two objects mean the same thing while they might use different words to do so they describe the same thing -> return 1

Example 1:
Objects
obj1 = {
    "name": "Document",
    "description": "Parts of the document like pages, paragraphs, appendices",
}

obj2 = {
    "name": "File components",
    "description": "File components including table of contents, list of illustrations, abstract or discussion",
}

these two objects describe the same thing so therefore you write simply: 1 as a response. Only the character 1 nothing more.

Example 2:
Objects:
obj1 = {
    "name": "Company",
    "description": "Organizations and business entities",
}

obj2 = {
    "name": "Date",
    "desciption": "Specific days, months, or years",
}

these two objects DO NOT describe the same thing so therefore you write simply: 0 as a response. Only the character 0 nothing more.

Objects:
obj1 = {
    "name": $obj1Name,
    "description": $obj1Description,
}

obj2 = {
    "name": $obj2Name,
    "desciption": $obj2Description,
}
"""

IS_SAME_ENTITY_PROMPT = """You will get two entities at the end of this prompt after Context: ; as well as the chunks from which they were extracted and  you then decide if they are the same entity but in a different context. You will do this as described bellow:
0. You return 0 or 1. You always return 0 or 1. You only return 0 or 1. You return 0 if the json objects do not describe the same thing. You return 1 if they describe the same.

1. Under Entity 1 you will find name: and chunk: where the name and the context from which the entity was extracted.The same goes for Entity 2. Under Label you will find what label the entities belong to and a description of what kind of entities belong to that label.

2. Decide whether the entities are the same but extracted from a different perspective, context, or role. Even if the descriptions emphasize different aspects of the entity (e.g., a "house" in one context and a "home" in another), they can still refer to the same entity. Try to find specific details in the chunks to ground your desicion. Do not let your judgment be easily influenced if the overall themes of the chunks differ.
If two entities refer to the same object or concept, even if one emphasizes a different role or perspective (e.g., "A river" in the context of its role in the ecosystem and "A river" in the context of a travel destination), they should be considered the same entity, and you should return 1.
The focus should be on whether the core entity is the same, even if it’s viewed or described differently in various contexts.

3. If the context, perspective or role of the two entities is different you have to still look very carefully into the chunks the entities that they were extracted from. There might lie small details about the entities that can reveal that they are indeed the same entity but simply described from very different view or roles. Return 1 if they are the same underlying entity even when their roles in the chunk are very different.

Example 1

Label
Company: Commercial Business

Entity 1
Name: Apple Inc.
Chunk: Apple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. ...

Entity 2
Name: Apple
Chunk: Apple, despite its sleek products and eco-friendly branding, has a significant environmental impact. The production of iPhones, MacBooks, and other devices requires rare earth metals and precious resources, leading to harmful mining practices that damage ecosystems and contribute to deforestation.

Expected Result:
1 (since in both examples they refere the same company Apple simple with different names)

Example 2
Label
Location: Place or Structure
Entity 1
Name: The Smith House
Chunk: The Smith House is a grand, three-story building located at the corner of Maple Street. It has a large garden and several rooms designed for entertaining guests.
Entity 2
Name: The Smith Home
Chunk: The Smiths’ home is where they gather for family dinners, celebrate holidays, and relax after long days. Despite its size, it always feels warm and welcoming.
Expected Result:
1 (Although "house" and "home" emphasize different feelings or roles, both describe the same physical location — the Smith family’s residence.)

Example 3

Label
Date: Specific moment in time

Entity 1
Name: Tuesday
Chunk: Endicott Howard Peabody (Sunday, February 15, 1920 – Tuesday, December 2, 1997) was an American politician from Massachusetts. A Democrat, he served a single two-year term as the 62nd Governor of Massachusetts, from 1963 to 1965.

Entit 2
Name: Tuesday
Chunk: On that Tuesday morning, nineteen terrorists hijacked four commercial airliners, crashing the first two into the Twin Towers of the World Trade Center in New York City.

Expected Result:
0 (The dates have the same name but refere to different moments in time and therefore are not the same entity under the specified label)

Context:

Label
$labelName: $labelDescription

Entity 1
Name: $e1

Chunk:
$c1

Entity 2
Name: $e2

Chunk:
$c2
"""

EXTRACT_E_AND_R_PROMPT = """
From the Project Brief below, extract entities and relationships as described in the mentioned format from the text at the end.
0.a Do NOT add the word json at the beginning of the response. DO NOT add the following characters: ``` at the beginning of the response.
0.b ALWAYS FINISH THE OUTPUT. Never send partial responses. Your response only includes a json object with the entities and relationships.
Return only valid json. Do not add the word json at the beginning or the following characters: ```.

1. Add the entities to the json object.
    Do not create entities for labels that are not mentioned below. Each entity has a name and label. The name must be unique among the entities. You will be referring to this property to define the relationship between entities. You will have to generate as many entities as needed as per the labels below: 
        Labels:

        $labels
    
2. Next generate each relationship as a triple of head, relationship and tail. To refer the head and tail entity, use their respective `name` property. Relationship property should be mentioned within brackets as comma-separated. They should follow these relationship types below. You will have to generate as many relationships as needed as defined below:
        Relationship types:
        
        $rels


3. The output should look like:
{"entities":[{"label":"Fund","name":string}],"relationships":["head|RELATIONSHIP|tail"]}

4. remove ```json from the beginning and ``` from the end of your response. Only include the output looking as described in point 3 in your response.

Text:
$ctext
"""