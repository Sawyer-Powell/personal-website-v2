---
title: Thoughts on the Economics on AI and Copyright
artist: alariko
hero: https://cdna.artstation.com/p/assets/images/images/079/702/348/large/alariko-img-20240802-175045-178.jpg?1725576581
artist-page: https://www.artstation.com/alariko
date: 2024-10-03
visible: true
tags:
  - econ
  - ml
---
Generative AI models, like ChatGPT, DALL-E, and others, are [known](https://harvardlawreview.org/blog/2024/04/nyt-v-openai-the-timess-about-face/) to have incorporated copyrighted works into their training data. These models provide facilities to generate completely new works that are similar, but not the same, as those they were trained on. In some cases models *cannot* produce output that exactly matches their training data. Text, images, video, and audio that generative AI models produce don't fit the official legal definition of a *derivative work*, which would put them in violation of copyright. Having your hard work used to train an AI, without your consent, and without compensation, can feel like theft. In much the same way that internet piracy feels like robbery. But, AI models give the appearance of mimicking human intelligence. As people, we read, watch and listen to copyrighted works. What we've consumed informs and teaches us how to create new art, movies, music and literature. So, if we are to say that AI models are violating copyright, or are breaking fair use, how can we argue that the basic process of our own creativity isn't?

# AI Eliminates the Moat of Copyright

Let's create a news website with articles entirely written by AI. Feed a large language model (LLM), like GPT-4o, all the articles from the New York Times. Fine tune this model to produce articles that match the NYT's style and tone. Everyday, pull the top articles from the New York Times. Use another large language model to pull out each article's key pieces of information.

This produces a collection of articles alongside cliff notes on what they cover. At this point we've preserved none of the original content that was in those articles. Only the critical facts and information. Take these bullet points and feed them into our NYT AI and ask it to generate full articles. This model will produce a series of well written news articles, with relevant information, that provides a simulated experience of reading an actual NYT article. This is a fully fledged news site created without having to pay a single journalist. Something we can easily build within few afternoons of work, and a couple dozen dollars in API credits.

This feels unethical. But, if a human did the same thing, reading news articles across the web, and writing their own articles based on that reporting, its clear that this is not a violation of copyright. This is a person producing a new work, not copying an existing one. In both cases, writing a news article parroting information from another source can devalue the work of the original journalist. However, it's critical to understand that the AI is able to extract the *value* of work done by New York Times journalists at an *industrial scale*.

# The Value of Information
The purpose of copyright, for all its strengths and weaknesses, is to make markets for non-scarce things possible. These markets are vital, because without them, professional songwriters, journalists, programmers, artists, etc. have few alternatives for income. Copyright allows artists and companies to create novel pieces of work, on which they can enforce an artificial scarcity. Copyright is similar to patent law, where patent law creates a scarcity around who can capitalize on ideas. Copyright grants its owner the sole rights of distribution. Without copyright, music, ideas, code, could be copied and replicated infinitely without consequence. This artificial scarcity, coupled with demand, creates markets for things which are fundamentally non-scarce. 

What are these people actually selling? They're selling information which contains a certain amount of *value*. This ineffable value is what makes that information desirable for a customer. Before AI models, the only way to duplicate that value, was to duplicate the information, to make a copy of the work. Hence the strength and motivation of copyright. You can argue that a person could come along, listen to all the songs from a musician, and create music that is highly inspired by them, but distinct. It could be argued, that by learning to produce similar music to that musician, they are stealing their ideas and devaluing their work. But this is a *good* thing. In the context of the music industry, this is competitive behavior.

- Musicians can create songs that are highly similar stylistically to other musicians, but if they create a song that is *sufficiently* the same as another, they are in violation of copyright. I.e. singing a song that has the same lyrics, melody, and chord progression, and selling that without the original musician's consent.
- Musicians creating similar music to each other is called a *genre*. Musicians operating within a genre are encouraged, by the design of copyright, to create distinct, compelling works that diversify them from other musicians in that genre. The best musicians push the boundaries of their genre. They make significant stylistic contributions to their musical culture.
- This competitive landscape pushes professional musicians to continually build a moat around the production of their art, to build an edge, an identity. To do something distinct that is very hard for another *person* to copy.
  
In order for copyright to do its job, it needs to be possible to have a protected competitive landscape for creative work. If someone wants to become a professional musician, or journalist, they need confidence that they can build a sustainable career.

# Industrial Scale Value Extraction

Key to the competitive market working is that it is possible for a musician, artist, journalist, etc, to create work that is *hard* to replicate. As we saw with the New York Times example, AI makes it *easy* for any creative work to be replicated. Not only is it easy to do, but it's easy to do at enormous scale. A skilled programmer can write something which not only replicates the New York Times, but also CNN, Fox News, Reuters, etc. in a week or less. The same applies to music using models like Suno.

If people are unaware that those articles are generated by AI, they will be receiving a similar amount of value to what they would get from the original works. Its not hard to see how this radically changes the competitive landscape for journalism. We need new market mechanisms and regulations to preserve creative markets.

# People Are Entitled to Their Work's *Value*, Not Just Its *Copies*
If a person produces a work, copyrights it, and that copyrighted work is then used to train an AI, that person should be entitled to a share of the value produced by the AI. A simple starting point is, if the AI was trained on 100 megabytes of that person's copyrighted work, and the AI was trained on 1000 megabytes of data in total, that person should be entitled to 1/10th (divided by some number to account for the value added by training the AI) of the revenue generated by the AI. This, or the original author of the work agrees to some settlement with the company for them to use their data.

To make this possible, if a company wants to sell an AI product, they need to provide detailed documentation on what data they used to train it.

If they then want to use their AI model to create another AI model, using generated data. I.e. they train a model to produce news articles, and train another model to mimic that news producing AI. If they chooose to sell that derivative AI, they're still obligated to report the source data that was used to train all the AIs in their whole system. Most of the value of their models *comes from* that original training data. That company should be forever obligated to compensate the creators of that data, as long as their commercial products use it.

This is not a simple task, but not an impossible one. To achieve this kind of a paper trail we would likely need open internet platforms for people to buy and sell training data. Alongside government intervention to ensure that companies selling AI products are compensating those who created the data. We also need stricter laws to put ownership of data back in the hands of those who create it. Non copyrighted data, like social media posts, emails, text messages, are fair game for tech companies to train AI models.

# A Better Data Economy

As we work on AI policy, we should be laser focused on creating a data economy where creative work is fairly compensated, while still allowing society to reap the enormous benefits of large AI systems. Designing regulations are hard because you want to preserve competitive behavior, while mitigating the consequences of open competition. Deferring large sums of money to the people who created the training data reduces incentives to create large new AI models. While keeping the status quo allows AI companies to consume entire sectors of the economy, concentrating money and power. Much of the investment in AI right now is *predicated* on the fact that this concentration is possible. Independent creative professionals could potentially make significant passive income from large AI systems. Even if the data they provided to OpenAI makes up one one-billionth of ChatGPTs training data, if OpenAI is serving millions of requests per second, their compensation amount could add up quickly.

If we don't implement modifications to copyright law, there will likely be be huge negative economic, and social, ramifications. However, if we modify the law smartly, we could see a massive infusion of money into the hands of creative workers. Importantly, when we think about AI policy, we need to think about how to preserve the spirit, but not necessarily the details, of copyright law. Focusing on the fundamental mechanism of copyright, how creative workers protect the *value* and ownership of their work is vital.
