---
title: "Case Study: ML Powered Product Substitutions"
artist: paul kidby
hero: https://www.paulkidby.com/wp-content/uploads/2016/01/gallery_2-650x884_c.jpg
artist-page: https://www.paulkidby.com/
date: 2024-11-14
visible: true
tags:
  - ml
  - swe
---
Recently at Counterpart I've had the opportunity to work with a medical supply company that helps doctors offices optimize their spending. This company takes a list of products that a clinic is currently buying and suggests substitutions for each product that is of equal to or lower cost. Because of some (disconcertingly serious 😐) inefficiencies in the market for medical supplies, clinics can often save double digit percentage points off their original expenditure. This is big business for a small company, but it's a process that's almost entirely manual. The database out of which they can recommend new products contains around a quarter million unique items. Over the past two months I've been building a system that can automatically make these substitutions with greater than 70% accuracy in one-shot scenarios on products it has never seen before, and over 92% accuracy when the system can suggest 5 substitutions. So, how do you build a system like this? How do you make it scalable and fast? Let's start engineering!

# The Simplest and Cheapest Approach

Instead of having the employees at the company manually go through their master list of products to find an appropriate substitution, we can design a piece of software that allows them to search across that master list.

The two easiest approaches would be to implement keyword search, or a fuzzy matching algorithm like levenshtein distance. Employees could enter keywords from the product description or title, and find products that have matching words. The fuzzy matching approach would be better at handling letters and phrases being out of order. It would also excel at handling small typos and misspellings in the data.

These approaches will certainly offer some efficiency gain for the employees, but they are still expected to have in-depth technical knowledge of the products they're working wit. Often times product names provided by a client will differ greatly from the product names in the database. Employees have to **know** what they're looking for ahead of time.

Here's an example of what a hard substitution could look like:

`CONTAIN  SPC N/S W/LID 4OZ` 

is substituted for 

`ManDaq RMS f/Adv Gyn & Surg` 

Based on results I've seen, using levenshtein distance will provide around a 5-10% accuracy at best.

# A Machine Learning Approach

Clearly there are nuances in how substitutions are made. Making effective substitutions requires some level of domain expertise in the meaning of the medical terms. Effective substitions also require a sense of how to suggest an item that is **almost** the same, but provides a much better value. An example of this would be buying blue towels from one manufacturer instead of tan from another. This means data beyond just the product description is critical to making substitutions. Luckily, we have a lot of historical data on substitutions this company has made in the past. The challenge ahead is leveraging that data effectively.

We need a to devise a system that allows employees to provide product information they've received from a client, and receive a list of products from this company's master list that are good substitutions. A straightforward approach to this problem is to create an **embedding model**.

The model will accept as input either the product information from a client, or from the master sheet, and spit out a big vector of floats. The model should be trained such that vectors produced by substitutable products are separated by a very small angle. Ideally, substitutable products produce vectors that are collinear.

Once this model is trained, we can go over every product in the master list and generate an index using the products' corresponding vectors. Every time we receive a product from a client, we query that index, finding items from the master list that are the most collinear with our client provided product vector. We can leverage libraries like `faiss` from Facebook to perform fast GPU powered vector search over that index.

## Cleaning our Data

The data is provided to us in excel spreadsheets. These spreadsheets contain information about a client's products (description, unit of measure, price, manufacturer, etc.) and an id to the item it was substituted for in the master list. Before doing any machine learning we should collate all of the client products across all of the spreadsheets, and match them to their corresponding item in the master list.

Using the `pandas` library to parse and collate all the spreadsheet information, we end up with a `DataFrame` with these columns: 

```
manufacturer
description uom
uom_price
schein_num
mfg_num
master_manufacturer
master_description
master_uom
master_size
master_strength
master_uom_price
master_mfg_num
file
sheet
```

The first five columns are the client product information, the following seven columns are the substitution made from the master list, and the final two contain information on where this data was extracted from.

Before using this to start learning, let's split the data into three parts: a set of data we'll use for training, a set of data we'll use for validation while training, and a test set that we won't touch at all for the entire learning process. For this project I went with a 60/20/20 split across these categories.

After cleaning and processing the data we end up with three csvs: train.csv, validation.csv, and test.csv.

## Establishing a Baseline

Hugging Face provides a number of great embedding models that we can start experimenting with. Notable among these is [minilm](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), a sentence transformer embedding model that has great performance at a relatively small footprint. The fact that it's a sentence transformer is great, since it means the vectors produced by this model can effectively encode deep semantic relationships between words.

After following the instructions provided in the page for `minilm`, we can start passing through all of our product descriptions from the training set and master list. We use the vectors from the master list to form an index using `faiss`, and use the vectors from our training set to query that index.

The response to the query is our model's prediction for how to substitute that client product. Using `minilm` as is, without any fine tuning, yields us about 10% accuracy on the training set. Better than traditional text querying, but far off from being genuinely useful. To get better performance we need to fine tune the model.

## Fine-tuning `minilm`

Luckily, `minilm`'s authors include source code in their HuggingFace repo which details how they trained the model. The training of `minilm` is based around a few key principles:

1. Prepare all of your sentences alongside an example of a sentence that should match the previous sentence, an a sentence that should not match. The matching sentence is the *positive* example, the non-matching sentence is the *negative* example. The original sentence is called the *anchor*.
2. Use the model to produce vectors for the positive, negative, and anchor sentences.
3. Compute scores for how *similar* the vectors are to each other, this is computed by taking the dot product of the anchor with the postiive and negative examples.
4. Computing the loss is treated as equivalent to a classification problem. We have a score for the positive example, and a score for the negative example. Applying `softmax` to these scores allows us to treat them as probabilities. I.e. the model predicts the positive example is the correct substitution at 70% confidence, and the negative at 30%. Since this is a classification problem, we can make use of *cross-entropy-loss*.
5. Once loss is calculated, we can do a backward pass on the network.

A very clever part of the design of `minilm` is that for step 4 it takes advantage of the fact we're passing **batches** of examples through the network every pass. The classification problem is not just against the positive and negative example associated with the anchor, it's against the positive and negative examples across *all* the anchors in the batch. So, if our batch size is 32, we're comparing each anchor against **64** candidates.

`minilm` uses the `AdamW` optimizer from PyTorch, alongside a learning rate scheduler. Both useful for training deep networks. Using this strategy to fine tune the network on product descriptions, we are able to reach around 30% accuracy. A huge improvement!

## Modeling More Than Just the Description

Clearly just matching over the product description is **not** enough to fully capture the process of making substitutions. Information like the manufacturer of the product, the price of the product, and the manufacturing number for the product could all play an important role.

Currently our model is just a fine-tuned version of `minilm`, but features like *price* are not going to fare well if we just include them in the product description. We need a way to include `minilm` in a larger neural network so that product description information can interact with price information.

For this next iteration of the model the outputs of minilm are combined with (normalized) price information and are fed into a 3 layer deep fully connected network, with each layer containing 400 nodes. The layer depth and node size is somewhat arbitrary, and was tuned based on metrics like training speed, and subjective measures of model quality. The output layer is also 400 nodes. Nothing changes in how we calculate loss and do backpropagation.

Another note about this iteration is that we can combine the product description information with the manufacturer and UOM information in the input to `minilm`. This is done by just concatenating these strings together. A cheap trick to avoid having to model these inputs out separately, but one that ends up working quite well in the end. This strategy is able to yield us around 40% accuracy.

## Re-examining the Training Process

Key to our process is the notion of a `negative` example for each of our anchors. At the moment, these negative examples are chosen randomly from our master list. But, what if we could ramp up the difficulty of the negative examples over the course of training? What if we can start with random negatives, but over time replace all the random negatives with *incorrect* predictions from the previous epoch. This way the model can focus on learning the minute differences betweeen products in the final stages of training.

At the end of each training epoch we use our model to index a random subset of the master list. We index a subset since indexing a quarter million products at the end of each epoch would be far too slow. This subset is designed such that for every anchor in the training set, the subset of the master list is guaranteed to contain the corresponding substitution. The rest of the data from the subset are randomly chosen products.

Once we've indexed the subset, we make a prediction for every product in the training set, and note every prediction the model got wrong. For every product in the training set we predicted incorrectly, we can randomly choose to include it as that product's negative example in the upcoming epoch. This random choice is driven by a probability that we determine. This probability represents the *difficulty* of the upcoming epoch.

At the beginning of training we start with a *difficulty* of 0, and then after a quarter of the way through training (after the learning rate scheduler has started to decay the learning rate) we can start ramping up the difficulty. I chose for the difficulty curve to exponentially increase up to 100%, giving a slow roll out of difficulty increases in the beginning, with a sharp increase in difficulty at the end. This strategy made a huge difference to performance, allowing the model to reach 60% accuracy.

## Paying Attention To Manufacturing Number

The final piece of the puzzle is the manufacturing number. This is a unique number that manufacturers give to their products which is often useful for finding an appropriate substitution. Manufacturing number is really important in situations where you need to select one product out of a list of very similar products. However, sometimes the manufacturig number is not helpful at all, since the subsitution suggested is from a completely different manufacturer.

The simplest way to incorporate the manufacturing number would be to concatenate it to the end of the string we're passing through `minilm`, and hope that it figures out what to do with it. Since this project is both work, and a learning experience, I was curious to see what would happen if I explicitly modeled the manufacturing number. To explicitly model manufacturing number I created a simple ASCII tokenizer, which takes the manufacturing number string and encodes it as an array of integers representing the corresponding character's ASCII code. These integers are then normalized to floats around 0, to prepare them to be sent through the network. I then included this normalized vector as an input into the first fully connected layer of the network, alongside the minilm output and the price output.

At first, training did not succeed. Explicitly modeling manufacturing number led to what I would call *training collapse* once we the *difficulty* started increasing. Once difficult negative examples started to be included, accuracy metrics during training started to plummet. I realized that this is likely caused by the model overfitting to the manufacturing number in the early phases of training.

The trouble with explicitly modeling manufacturing number is that the manufacturing number is only useful in *some* circumstances, for *some* products. But in the model above, manufacturing number is treated as important in *all* circumstances. The key to solving this problem is to realize that we can use the output from minilm as a mechanism for the model to *attend* to the manufacturing number. We need some structure in the network that allows it to selectively pay attention to the manufacturing number.

Doing this is relatively easy, and well documented. We just create an attention mechanism within the network. Basic attention mechanisms are surprisingly simple. To leverage it in our network we simply: 

1. Take the dot product of the `minilm` output and the vectorized manufacturing number
2. Normalize that dot product, often times using `softmax`
3. Take that normalized score and multiply it against the vectorized manufacturing number.

Notice that this step of taking the dot product allows the `minilm` outputs to define a coefficient on the magnitude of the manufacturing number vector. This is what allows the `minilm` outputs to control how much the model pays "attention" to the manufacturing number.

One caveat here is that the `minilm` outputs and the manufacturing number need to be the same dimension for the attention mechanism to work. This is easily solved by projecting both vectors to the same dimensionality before computing the attention score.

This approach led to our best and current accuracy of 70% in one shot scenarios against completely foreign data, 92% in a five shot scenario on the same data.
