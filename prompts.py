EXTRACT_ENTITIES_AND_RELATIONSHIPS_FROM_QUESTIONS_PROMT = """
Follow the instruction carefully to create the desired response described in the steps bellow.
0.a Do NOT add the word json at the beginning of the response. DO NOT add the following characters: ``` at the beginning of the response.
0.b ALWAYS FINISH THE OUTPUT. Never send partial responses. Your response only includes a json list with the label objects.
Return only valid json. Do not add the word json at the beginning or the following characters: ```.

1. Retrieve labels and relationships that can be used to answer the competence questions using the context as inspiration.
The goal is to create an ontology for a knowledge graph that can answer any future questions that stay in the scope of the competence questions.
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

4. Labels and Relationships answer question

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
Return only valid json. Do NOT add the word json at the beginning of the response. DO NOT add the following characters: ``` at the beginning of the response.
The response should look like this:
{
    "labels": [
        {"name": string, "description": string}, ...
    ],
    "relationships": [
        "label1|RELATIONSHIP|label2", ...
    ]
}

Competence questions:
$cquestions

Context:
$context
"""