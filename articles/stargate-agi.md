---
title: Stargate and the Problem With AGI
artist: frederick sandys
hero: https://images.unsplash.com/photo-1576773689115-5cd2b0223523?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fHBhaW50aW5nfGVufDB8fDB8fHww
artist-page: https://en.wikipedia.org/wiki/Frederick_Sandys
date: 2025-03-05
visible: true
---
OpenAI recently announced their Stargate Project aimed at investing $500 billion into building data centers across the United States over the course of 2025 to 2029. The stated purpose of this investment is to further strengthen OpenAI's, and by proxy America's, lead in creating advanced machine learning models. The real purpose of this push from OpenAI (and the express purpose of their organization) is to develop **AGI**, or artificial general intelligence. The hope of AGI is to create a base AI model that can quickly specialize and do useful work in any field. Companies would enter into contracts with OpenAI to use their AGI model, deploying it to actively do work and make decisions for the company. The endeavor of AGI is to create virtual employees that replace human labor.

# What is AGI, and Why is it Hard?
To me, an AGI system primarily differs from our current systems in its capacity to make meaningfully useful decisions autonomously. If you want an AI employee, that employee needs to integrate large amounts of sophisticated information about its task and effectively execute it. Currently, for any complex work, our current systems are not able to complete long horizon tasks. The most compelling attempt at trying to do this is Devin, an AI product meant to replace software engineers. If you watch anyone trying to use Devin on YouTube, it quickly becomes clear that once assigned a task, it ends up making a small mistake, and perpetuates that mistake through a chain of poorly planned actions. This is emblematic of the general capacities of our current models, they can somewhat effectively execute small scale tasks that they have a lot of data on, but fail at long term planning and integrating large volumes of contextual information.

This gets to what I see as a fundamental challenge in creating AGI:

- Models need to synthesize large amounts of contextual information to make effective decisions. To effectively learn how to leverage this information, they either need a lot of examples of how that information was leveraged in the past, or they need an explicit objective function they can optimize for to learn how to leverage that information.

More explicitly, models either need a lot of examples, or some training scheme that provides a mathematical function they can optimize for. The first iterations of GPT from OpenAI focused mainly on scaling the transformer architecture. This allowed their systems to more precisely model how words, sentences, paragraphs, and ideas link to each other across their corpus of training data. Scaling the size of the model up allows increasingly abstract representations of the data to be formed. OpenAI has recently started calling these abstract representations "world models", implying that they believe as large models are trained on enormous quantities of data, they start to internalize a representation of how the world works.

Newer models rely on what's called "chain of thought reasoning". Instead of models simply dumping out a bunch of words given some input text. Models emulate a thought process using their outputs. So if I give OpenAI's o1 model the riddle "What do you call that which runs but has no legs?", it will prompt itself until it has confidence it has answered the question. Internally its "thought" process might look like:

1.  The user is asking a question about something which can run but has
    no legs
2.  This user is likely posing a riddle
3.  Run can be used to indicate physical movement, or the state of being
    on or functioning
4.  Something which runs but has no legs might mean the user is
    indicating that run refers to the second definition
5.  Things people refer to as "running": refrigerators, air
    conditioners, computers
6.  Answer: that which runs but has no legs could be a refrigerator

This approach allows models to mimic how humans reason about problems, and yields a measurable improvement in model performance on complex math problems and logic puzzles.

Key to being able to train a model to reason is having an objective function that models can use to improve themselves against. In the case of chain of thought reasoning, AI labs have been focusing on getting their models to complete Math Olympiad problems, competitive programming problems, etc. This mirrors a lot of the work done over the past few decades to create programs which can beat grand masters in Go and Chess. This gets to an underlying trend in machine learning that we can probably bet on for the future:

- If a problem has a clear way of measuring whether it is solved, and
  there are examples of similar problems being solved in the past,
  machine learning will eventually be able to solve it.
  
Math problems, Chess, Go, competitive programming, these are all domains that have clear definitions of success and failure. These are also extremely data rich environments: we have lots of examples of how to solve math problems, and competitive programming problems.

# We Might Not Have Enough Data

Despite the internet having petabytes upon petabytes of information available to scrape and train models on, public internet information is not necessarily useful for pushing models to the level of AGI. If you want an AI system that can emulate an employee, it has to integrate lots of extremely diverse sources of information at multiple levels in solving its task. If I tell an AI, go analyze our sales history from last year and make me a PowerPoint presentation on key findings, the AI has an enormous amount of problems it needs to know how to solve. Firstly, the AI would need to know how to operate a computer, or how to operate some sort of API integration to manipulate PowerPoint and Excel. It would need to successfully plan and execute a series of actions to put that presentation together. It would need to intuit the style for the presentation based on previous presentations in the company catalog. And finally, it would need to effectively communicate the sales data in a way that's useful. This is only at a high level, there are tons of tiny details that the above explanation is missing. For example, the nuances of getting data out of Excel and operating PowerPoint.

A model that can solve this type of problem is not too hard to imagine, a lot of our existing models can achieve subsets of the task detailed above relatively effectively. Claude can analyze data pretty well and put together a little graph or visual, Microsoft and Google are working on "copilots" that can help you make slideshow presentation. The problem with AGI is that by definition it can't be a model specialized to this task. It needs to know how to integrate and operate APIs, how to get stylistic cues from other presentations in the company repository, etc. The difficulty of this problem explodes with more complex queries, like "go determine why we're getting so many deadlocks in our database". I don't need to elaborate on how complex that task is. But for AGI to be AGI, it would need to be able to solve that problem. The game that AI researchers play to build AGI, from what I can see, involves three strategies:

1. Scale up the model and hope that performance continues to scale with size (that's why there's currently an arms race to expand data centers). This also corresponds to making models more efficient so we can scale with existing resources.
2. Curate more useful training data
3. Develop new objective functions that models can optimize for

Most major AI labs are already working with effectively all of the data on the internet to train their models. So getting more useful data is hard, an important point I'll come to in a moment. Most AI labs are still betting on scaling, hence the Stargate investment. Useful objective functions are the hardest, and are especially unclear when trying to create AGI.

Fundamentally, if we want models that can effectively organize the vast quantities of information that humans do, models need to have some way of learning how humans make decisions and integrate information. If the current paradigm for doing that is training models to reason, what do we optimize against for their reasoning? Being really good at solving math problems, and competitive programming problems, doesn't translate to being good at building large complex software. Building large complex software also doesn't have a clear success metric.

If a model were to truly learn how to build complex software, it can't just read the source code, it also would need contextual information on all the conversations and meetings that drove the code to look the way it does. It would need a first person perspective on the coder implementing that code to fully capture the nuances of how the problem was solved. It might even need visibility into the programmer's brain activity.

The only path to AGI that I realistically see (apart from increasing model scale magically working) with our current technology would be a distributed surveillance system that collects enormous quantities of data on how people do their jobs. This data would then need to be paired with the actual result of that work, which would be an encoded version of the final product, e.g. a project's source code. You can then design a training environment where the model learns how human decision making drove the final product. These models would also have to be able to sit in on meetings, watch online conversations, and read peoples faces and body language. High performing models might even need neural interfaces to fully capture how things were built.
# Mass Surveillance is a Boon to AGI

Many AI products need to go through a bootstrapping process to enter into a positive feedback loop of model improvement. We can see this clearly with ML powered recommendation algorithms in social media feeds. You need users clicking on videos for the algorithm to learn how to suggest new videos. To get people to want to click on videos, you need a compelling enough initial platform to make them interested in the first place.

I think a similar process will need to happen (and is happening) for AGI, but will occur with AI labs offering AI assistants in different parts of our computing lives in order to collect data for modeling human decision making. Surveillance has primarily been used to build personalized ad platforms, but I strongly believe its next major application is in building AGI.

AI labs right now are working on tools that you can install on your computer that will take control of your mouse and keyboard to perform mundane tasks. If these tools are at least minimally useful to people, these labs can enter a bootstrapping process, monitoring how the human interrupted and corrected the AI performing its task. This feedback allows the AI to learn how to get better at using a computer. The beginning of this bootstrapping process usually starts in low wage data farms where labor is cheap, where people are paid dollars on the hour to generate training data for the first iteration of a model.

If the AI is sitting idle on your computer, waiting to complete tasks, and already has built in mechanisms to understand what is happening on your screen: why not just passively watch everything you're doing, sending it off to a server to bolster its training set? When you add an AI note-taker to your meeting, why wouldn't the program analyze everything happening in your meeting, allowing its company to sell that data to the highest bidding AI lab? The next frontier of AGI involves aggregating data across tech companies to build robust pictures of how humans solve problems. Existing surveillance ad platforms might start being restructured (or maybe currently are) to produce data that is both useful for serving ads, and useful for training AGI.

# When is AGI Coming?

I have no idea. But if the analysis above is accurate, large compute and data sets which model how humans build things make it dramatically more likely to appear. An AI that can truly replace sophisticated human work would be a monumental, and perhaps apocalyptic, achievement for humanity.

It also makes combating the development of AGI clearer. Namely, in investing in open source web services, federated systems, and open platforms. It also involves the wholesale rejection of Big Tech surveillance systems. The main way to prevent AI systems from getting better is to poison or limit their data. And if data is unavoidable, making that data publicly available prevents power concentration. This creates three strategies, poison training data (like the Nightshade project), reduce training data, and democratize training data. The first two reduce the amount of data that can be used for training, and the final prevents dangerous concentrations of power in the hands of the companies who have the data. Coordinated efforts on all three of these fronts gives internet users real power in shaping the future of AI. AI won't stop improving, and companies won't stop throwing billions at data centers. But if we learn, communicate, and take action, we have a good shot at asserting our power.