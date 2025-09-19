AI Is Not Software
by Davidmanheim
2nd Jan 2024
https://www.lesswrong.com/posts/iknSNTbb8deJwQuLJ/ai-is-not-software

Epistemic Status: This idea is, I think, widely understood in technical circles. I'm trying to convey it more clearly to a general audience. Edit: See related posts like this one by Eliezer for background on how we should use words.

What we call AI in 2024 is not software. It's kind of natural to put it in the same category as other things that run on a computer, but thinking about LLMs, or image generation, or deepfakes as software is misleading, and confuses most of the ethical, political, and technological discussions. This seems not to be obvious to many users, but as AI gets more widespread, it's especially important to understand what we're using when we use AI.

Software
Software is how we get computers to work. When creating software, humans decide what they want the computer to do, think about what would make the computer do that, and then write an understandable set of instructions in some programming language. A computer is given those instructions, and they are interpreted or compiled into a program. When that program is run, the computer will follow the instructions in the software, and produce the expected output, if the program is written correctly. 

Does software work? Not always, but if not, it fails in ways that are entirely determined by the human’s instructions. If the software is developed properly, there are clear methods to check each part of the program. For example, unit tests are written to verify that the software does what it is expected to do in different cases. The set of cases are specified in advance, based on what the programmer expected the software to do. If it fails a single unit test, the software is incorrect, and should be fixed. When changes are wanted, someone with access to the source code can change it, and recreate the software based on the new code.

Given that high-level description, it might seem like everything that runs on a computer must be software. In a certain sense, it is, but thinking about everything done with computers as software is unhelpful or misleading. This essay was written on a computer, using software, but it’s not software. And the difference between what is done on a computer and what we tell a computer to do with software is obvious in cases other than AI. Once we think about what computers do, and what software is, we shouldn’t confuse “on a computer” with software.

Not Software
For example, photos of a wedding or a vacation aren’t software, even if they are created, edited, and stored using software. When photographs are not good, we blame the photographer, not the software running on the camera. We don’t check if the photography or photo editing worked properly by rerunning the software, or building unit tests. When photographs are edited or put into an album, it’s the editor doing the work. If it goes badly, the editor chose the wrong software, or used it badly - it’s generally not the software malfunctioning. If we lose the photographs, it’s almost never a software problem. And if we want new photographs, we’re generally out of luck - it’s not a question of fixing the software. There’s no source code to rerun. Having a second wedding probably shouldn’t be the answer to bad or lost photographs. And having a second vacation might be nice, but it doesn’t get you photos of the first vacation.

Similarly, a video conference runs on a computer, but the meeting isn’t software - software is what allows it to run. A meeting can go well, or poorly, because of the preparation or behavior of the people in the meeting. (And that isn’t the software’s fault!) The meeting isn’t specified by a programming language, doesn’t compile into bytecode, and there aren’t generally unit tests to check if the meeting went well. And when we want to change the outputs of a meeting, we need to reconvene people and try to convince them, we don’t just alter the inputs and rerun.  

Generative AI
Now that it should be clear that not everything that runs on a computer is a program, why shouldn’t we think about generative AI as software?

First, we can talk about how it is created. Developers choose a model structure and data, and then a mathematical algorithm uses that structure and the training data to “grow” a very complicated probability model of different responses. The algorithm and code to build the model is definitely software. But the model, like anything stored by a computer, is just a set of numbers - as is software, and images, and videoconferences. The AI model itself, the probability model which was grown, is generating output based on a huge set of numbers that no human has directly chosen, or even seen. It’s not instructions written by a human.

Second, when we run the model, it takes the input we give it and performs “inference” with the model. This is certainly run on the computer, but the program isn’t executing code that produces the output, it’s using the complicated probability model which grew, and was stored as a bunch of numbers. The model responds to input by using the probability model to estimate the probability of difference responses, in order to output something akin to what the input data did - but it does so in often unexpected or unanticipated ways. Depending on the type of model it learned and the type of training data, it finds the probability of different outputs. Some have called the behavior of such generative models a “stochastic parrot,” which explains that it’s not running a program, it’s copying what the training data showed it how to do. On the other hand, this parrot is able to compose credible answers to questions on the bar exam, produce new art, write poetry, explain complex ideas, or nearly flawlessly emulate someone’s voice or a video of them speaking.

Third, what do we do if it doesn’t do what we expected? Well, to start, what the system can or cannot do isn’t always understood in advance. New models don’t have a set of features that are requested and implemented, so there’s no specification for what it should or should not do. The model itself isn’t reviewed to check it is written correctly, and unit tests aren’t written in advance to check that the model outputs the right answers. Instead, a generative AI system is usually tested against benchmarks used for humans, or the outputs are evaluated heuristically. If it performs reasonably well, it's celebrated, but it is expected that it gets some things wrong, and often does things the designers never expected. And when changes are needed, the nearest equivalent of the source code - that is, the training data and training algorithm which were used to produce the system - is not referenced or modified. Instead, further training, often called “fine tuning,” or changes in how the system is used, via “prompt engineering,” is used to change its behavior. 

Lastly, we can talk about how it is used - and this is perhaps the smallest difference. The difference between Google running a program to find and display a stock photograph of what you searched for, compared to Dall-E 3 generating a stock photograph, might seem small. But one is a photograph of a thing that exists, and the other is not. And the difference between asking Google for an answer and asking ChatGPT might also not be obvious - but one is retrieving information, and the other is generating it. Similarly, the difference between talking to a person via video conference and talking to a deep fake may not be obvious, but the difference between a human and an AI system is critical, and so is the difference between an AI system and traditional software. 

To reiterate, AI isn’t software. It’s run using software, it’s created with software, but it’s a different type of thing. And given that it’s easy to confuse, we probably need to develop new intuitions about the type of thing it is.

Thanks to Mikhail Samin and Diane Manheim for helpful comments on an earlier draft.


 

New to LessWrong?
Getting Started

FAQ

Library


58
Mentioned in
48
Goodbye, Shoggoth: The Stage, its Animatronics, & the Puppeteer – a New Metaphor
36
Sufficiently Decentralized Intelligence is Indistinguishable from Synchronicity
28
The Logistics of Distribution of Meaning: Against Epistemic Bureaucratization
17
Terminology: <something>-ware for ML?
6
Superintelligence's goals are likely to be random
AI Is Not Software
31
gjm
3
Davidmanheim
10
the gears to ascension
4
Oliver Sourbut
2
Daniel Kokotajlo
2
the gears to ascension
1
Oliver Sourbut
9
noggin-scratcher
18
abramdemski
3
JBlack
2
Davidmanheim
1
Davidmanheim
1
noggin-scratcher
2
Davidmanheim
1
noggin-scratcher
2
Davidmanheim
7
[anonymous]
3
Davidmanheim
2
[anonymous]
3
Davidmanheim
2
[anonymous]
2
Davidmanheim
4
[anonymous]
3
zoop
3
jessicata
14
abramdemski
1
RogerDearnaley
0
Douglas_Knight
2
Davidmanheim
New Comment


29 comments, sorted by top scoring
Click to highlight new comments since: Today at 11:36 AM
[
-
]
gjm
2y
31
18
An AI system is software in something like the same way a human being is chemistry: our bodies do operate by means of a vast network of cooperating chemical processes, but the effects of those processes are mostly best understood at higher levels of abstraction, and those don't behave in particularly chemistry-like ways.

Sometimes our bodies go wrong in chemistry-based ways and we can apply chemistry-based fixes that kinda work. We may tell ourselves stories about how they operate ("your brain doesn't have enough free serotonin, so we're giving you a drug that reduces its uptake") but they're commonly somewhere between "way oversimplified" and "completely wrong".

Sometimes an AI system goes wrong in code-level ways and we can apply code-based fixes that kinda work. We may tell ourselves stories about how they operate ("the training goes unstable because of exploding or vanishing gradients, so we're introducing batch normalization to make that not happen") but they're commonly somewhere between "way oversimplified" and "completely wrong".

But most of the time, if you want to understand why a person does certain things, thinking in terms of chemistry won't help you much; and most of the time, if you want to understand why an AI does certain things, thinking in terms of code won't help you much.

Reply
[
-
]
Davidmanheim
2y
3
0
Yes, this is part of the intuition I was trying to get across - thanks! 

Reply
[
-
]
the gears to ascension
2y
10
3
just name it after another phase maybe lol. gelware? liquidware. fluidware? gasware? plasmaware?? etherware?!

Reply
[
-
]
Oliver Sourbut
2y
4
0
noware? everyware? anyware? selfaware? please-beware?

(jokes, don't crucify me)

I have a serious question with some serious suggestions too

Reply
21
[
-
]
Daniel Kokotajlo
2y
2
0
Deepnets?

Reply
[
-
]
the gears to ascension
2y
2
0
I think the goal of this naming party is to convey something to the general public, but regardless I was just going at it and not terribly trying to be strategic

Reply
[
-
]
Oliver Sourbut
2y
1
0
Hardware, software, ... deepware? I quite like this actually. It evokes deep learning, obviously, but also 'deep' maybe expresses the challenge of knowing what's happening inside it. Doesn't evoke the 'found/discovered' nature of it.

Reply
[
-
]
noggin-scratcher
2y
9
4
True to say that there's a distinction between software and data. Photo editor, word processor, video recorder: software. Photo, document, video: data.

I think similarly there's a distinction within parts of "the AI", where the weights of the model are data (big blob of stored numbers that the training software calculated). Seems inaccurate though, to say that AI "isn't software" when you do still need software running that uses those weights to do the inference.

I guess I take your point, that some of the intuitions people might have about software (that it has features deliberately designed and written by a developer, and that when it goes wrong we can go patch the faulty function) don't transfer. I would just probably frame that as "these intuitions aren't true for everything software does" rather than "this thing isn't software".

Reply
[
-
]
abramdemski
2y
18
5
Compare this to a similar argument that a hardware enthusiast could use to argue against making a software/hardware distinction. You can argue that saying "software" is misleading because it distracts from the physical reality. Software is still present physically somewhere in the computer. Software doesn't do anything hardware can't do, since software doing is just hardware doing. 

But thinking in this way will not be a very good way of predicting reality. The hypothetical hardware enthusiast would not be able to predict the rise of the "programmer" profession, or the great increase in complexity of things that machines can do thanks to "programming". 

I think it is more helpful to think of modern AI as a paradigm shift in the same way that the shift from "electronic" (hardware) to "digital" (software) was a paradigm shift. Sure, you can still use the old paradigm to put labels on things. Everything is "still hardware". But doing so can miss an important transition.

Reply
[
-
]
JBlack
2y
3
-3
Definitely agreed. AI is software, but not all software is the same and it doesn't all conform to any particular expectations.

I did also double-take a bit at "When photographs are not good, we blame the photographer, not the software running on the camera", because sometimes we do quite reasonably blame the software running on the camera. It often doesn't work as designed, and often the design was bad in the first place. Many people are not aware of just how much our cameras automatically fabricate images these days, and present an illusion of faithfully capturing a scene. There are enough approximate heuristics in use that nobody can predict all the interactions with the inputs and each other that will break that illusion.

A good photographer takes a lot of photos with good equipment in ways that are more likely to give better results than average. If all of the photos are bad, then it's fair to believe that the photographer is not good. If a photograph of one special moment is not good, then it can easily be outside the reasonable control of the photographer and one possible cause can be software behaving poorly. If it's known in advance that you only get one shot, a good photographer will have multiple cameras on it.

Reply
[
-
]
Davidmanheim
2y
2
0
I'm asking the question of how we should think about the systems, and claiming "software" is very much the wrong conceptual model. Yes, AI can work poorly because of a software issue, for example, timeouts with the API, or similar. But the thing we're interested in discussing is the AI, not the software component - and as you point out in the case of photography, the user's skill with the software, and with everything else about taking photographs, is something that occurs and should be discussed not in terms of the software being used.

Reply
[
-
]
Davidmanheim
2y
1
-1
We can play the game of recategorizing certian things, and saying data and software are separate - but the question is whether it adds insight, or not. And I think that existing categories are more misleading than enlightening, hence my claim.

For example, is my face being picked up by the camera during the videoconference "data" in a meaningful sense? Does that tell you something useful about how to have a videoconference? If not, should we call it software, or shift our focus elsewhere when discussing it?

Reply
[
-
]
noggin-scratcher
2y
1
0
I'm not certain I follow your intent with that example, but I don't think it breaks any category boundaries.

The process using some algorithm to find your face is software. It has data (a frame of video) as input, and data (coordinates locating a face) as output. The facial recognition algorithm itself was maybe produced using training data and a learning algorithm (software).

There's then some more software which takes that data (the frame of video and the coordinates) and outputs new data (a frame of video with a rectangle drawn around your face).

It is frequently the role of software to transform one type of data into another. Even if data is bounced rapidly through several layers of software to be turned into different intermediary or output data, there's still a conceptual separation between "instructions to be carried out" versus "numbers that those instructions operate on".

Reply
[
-
]
Davidmanheim
2y
2
0
I'm not saying that I can force breaking of category boundaries, I'm asking whether the categories are actually useful for thinking about the systems. I'm saying it isn't, and we need to stop trying to use categories in this way.

And your reply didn't address they key point - is the thing that controls the body being shown in the data being transmitted software, or data? And parallel to that, is the thing that controls the output of the AI system software or data?

Reply
[
-
]
noggin-scratcher
2y
1
0
Oh I see (I think) - I took "my face being picked up by the camera" to mean the way the camera can recognise and track/display the location of a face (thought you were making a point about there being a degree of responsiveness and mixed processing/data involved in that), rather than the literal actual face itself.

A camera is a sensor gathering data. Some of that data describes the world, including things in the world, including people with faces. Your actual face is indeed neither software nor data: it's a physical object. But it does get described by data. "The thing controlling" your body would be your brain/mind, which aren't directly imaged by the camera to be included as data, but can be inferred from it.

So are you suggesting we ought to understand the AI like an external object that is being described by the data of its weights/algorithms rather than wholly made of that data, or as a mind that we infer from the shadow cast on the cave wall? 

I can see that being a useful abstraction and level of description, even if it's all implemented in lower-level stuff; data and software being the mechanical details of the AI in the same way that neurons squirting chemicals and electrical impulses at each other (and below that, atoms and stuff) are the mechanical details of the human.

Although, I think "humans aren't atoms" could still be a somewhat ambiguous statement - would want to be sure it gets interpreted as "we aren't just atoms, there are higher levels of description that are more useful for understanding us" rather than "humans are not made of atoms". And likewise for the AI at the other end of the analogy.

Reply
[
-
]
Davidmanheim
2y
2
0
Yes, I think you're now saying something akin to what I was trying to say. The AI, as a set of weights and activation funtions, is a different artifact than the software being used to multiply the matrices, much less the program used to output the text. (But I'm not sure this is quite the same as a different level of abstraction, the way humans versus atoms are - though if we want to take that route, I think gjm's comment about humans and chemistry makes this clearer.)

Reply
[
-
]
[anonymous]
2y
7
-4
I am not sure this is correct. Actually I feel pretty confident it is not.

In the broader scope of systems engineering, especially for embedded control systems, every component has a probability less than 1.0 of working. A good system design factors in the likelihood of failure for any single component. Generally there are redundancies to improve the probability to a series probability. For example, the Tesla cybertruck uses 2 front steering motors, with 2 controllers, 2 network links, at least 2 steering angle sensors, and 2 power supplies. In order for the steering to fail at least one component in both systems has to fail during the same drive, or the fault has to be undetected in the A system at startup and the B system fails on the same drive.

Human engineers sit down and multiply probabilities for the above and add redundancy or more reliable components until the design satisfied a target pFail.

With ML models you know or can measure the following :

How confident is the model in its perception of the current situation. (Empirical, measured in training)
Is the current system input within the latent space of the training distribution (from a parallel model)
The neural sim that lockstep predicts n future environment states conditional on actions : how confident is it? (Empirical, measured in training on real data)
How costly are errors in the current situation?
In the current situation, what classes of error are likely? (For example an autonomous vehicle at 65mph draws from the "high speed collision" risk pool)
With this information it is possible to build an outer control algorithm that uses multiple ML models to accomplish a larger task. And this algorithm can use the above information to shut down the model or revert control to a safer policy (stop the robot, engage the brakes) when the risk is high. One obvious note: "confidence" and "in distribution" are empirical metrics measured during training, they are not a number the model can "choose" what to give in an agentic way.

This outer framework is software. It's how autonomous car stacks except comma.ai and donkey car work. The framework people put around their discord bots using AI is similar. The framework doesn't just let the model do anything it wants, it restricts model actions to discord messages but only when a keyword to trigger the bot is emitted.

For any use of AI, present or future that I can anticipate, human engineers will use software frameworks, with more restrictive frameworks and multiple parallel models for AI applications that have high risks.

Do you agree or disagree? If you disagree, do you acknowledge that this is how present engineers are doing this task? Why do you believe future designs will be less restricted?

Reply
[
-
]
Davidmanheim
2y
3
1
All of the abstractions you are using are just as relevant to system design for a factory, or a construction project. You could do all of the things you're discussing about system design for a mechanical system! And yes, present engineers are treating these systems like software, but to the extent they are doing so, they are missing lots of critical issues, and as we've seen, they keep needing to add on bits to their conceptual model of what they need to deal with in order to have it be relevant. (Which is why I'm saying we need to stop thinknig of it as software.)

So on your final set of questions, I certainly agree that the systems can be analyzed via similar approaches to system engineering, but I think talking about the AI systems as software is far less helpful than saying that are a different thing, with different failure modes, requiring a different conceptual model, and doing your systems engineering on that basis.

Reply
[
-
]
[anonymous]
2y
2
-2
You could do all of the things you're discussing about system design for a mechanical system! And yes, present engineers are treating these systems like software, but to the extent they are doing so, they are missing lots of critical issues, and as we've seen, they keep needing to add on bits to their conceptual model of what they need to deal with in order to have it be relevant. (Which is why I'm saying we need to stop thinknig of it as software.)

You are correct that systems engineering applies to all systems, including mechanical.

So you are saying that people will hand write a bunch of framework software around the AI, and deal with software issues. But they can't think of the AI software like you would wrap a library like say openCV, the AI components have their own issues you have to understand. And the example I gave where your wrapper software examines telemetry to decide when to take control away from the AI model requires you to understand the telemetry. For example, openCV as a library has no "confidence" or "incompressible input state".

So the engineer who are writing the software have to understand deeply how the AI modules work and better engineers will learn with experience how they tend to fail. So they are "AI software engineers" who write software, knowing current methods, and also deal with AI. This sounds kinda like a compression of their job role would just be to say they are specialist swes, contradicting your post title. Agree or disagree?

Do you agree at a systems level you still have to design the overall system to purpose, selecting more reliable components over the bleeding edge and choosing series probabilities when needed to reach the target level of reliability?

I ask this because this seems to be a rather large schism between people like yourself who understand what I am talking about, and the louder doom voices. I bring this up because there is something extremely obvious that jumps out if you actually try to model how a systems engineer would design an AI system with authority.

Can you allow the modules, which have an empirical chance of failing measured on some test (say millions of simulated miles of driving, or millions of hours in a warehouse), to self modify? Can you permit unfiltered and unstructured network messages to reach the AI modules? Are you going to use monolithic inscrutable ASI level models or simpler and more specialized models that are known to be more reliable?

I don't see how you could design a system, as an engineer using current techniques, that permits this, for any system with actual authority. (chatGPTs have no authority, vs say avionics that does)

If the AI module cannot update itself, and it cannot send messages to coordinate a treacherous turn with other AIs, it is difficult to see how this type of AI with authority will cause existential risk. Can you describe a realistic way this could happen, assuming the system was designed by system engineers with median present day competence?

Reply
[
-
]
Davidmanheim
2y
3
1
I'm not talking about AI doom right now, I'm talking about understanding the world. At the system level, you claim we need to design the overall system to purpose, and that's fine for controlling a system - but the same goes for when humans are part of the system, and we're using six sigma to reduce variance in process outcomes. And at that point, it's strange to say that more generally, humans are just components to control, and we can ignore that they are different than actuators and motors, or software scripts. Instead, we have different categories - which was the point originally.

Reply
[
-
]
[anonymous]
2y
2
0
When you say "humans are just components to control" what did you have in mind there?

"Engineered" systems that use AI have to be designed for a specific task or class of tasks and they aren't responsible for the actions of humans. For example an AI tutor for children isn't responsible for the long term consequences, it's responsible for kpis for reliability, and a low probability of inappropriate content or factually incorrect content appearing in the output. You might accomplish this today by generating several outputs with different temperatures internally and fact check/inspect the candidate output internally.

Something like a surgical system - maybe decades away - isn't responsible for the long term outcome, but instead is responsible for measurable parameters during the operation and post convalescent stay that are statistically correlated with future longevity. Once the patient leaves they are out of scope.

Both examples could have negative long term or global outcomes, in the same way human engineers who design a coal boiler don't care about the smoke after it leaves the stack.

Are you talking about humans discovering inputs that are adversarial and lead to system failure in the above, or are you talking about long term consequences to the world from narrow scope general ASI systems?

Reply
[
-
]
Davidmanheim
2y
2
0
In manufacturing or other high-reliability processes, human inputs are components which need the variability in their outputs controlled. I'm drawing a parallel, not saying that AI is responsible for humans.

And I'm completely unsure why you think that engineered systems that use AI are being built so carefully, but regardless, it doesn't mean that the AI is controlled, just that it's being constrained by the system. (And to briefly address your points, which aren't related to what I had been saying, we know how poorly humans take to being narrowly controlled, so to the extent that LLMs and similar systems are human-like, this seems like a strange way to attempt to ensure safety with increasingly powerful AI.)

Reply
[
-
]
[anonymous]
2y
4
2
In manufacturing or other high-reliability processes, human inputs are components which need the variability in their outputs controlled. I'm drawing a parallel, not saying that AI is responsible for humans.

Ok I think what you are talking about here is the second thing I brought up:

humans discovering inputs that are adversarial and lead to system failure in the above

For example an AI tutor may get exploited by humans finding a way to trick the tutor into emitting inappropriate content, or selling a car for $1.  https://news.ycombinator.com/item?id=38681450

And I'm completely unsure why you think that engineered systems that use AI are being built so carefully,

You have mentioned previously you have direct experience with Mobileye.  Their published videos explaining their design philosophy sound precisely like the architecture I describe.  Notably, their "true redundancy", where 3 separate AI models examine 3 separate sets of sensor inputs, and model the environment in parallel.  The motion solver part of their stack is going to assume the environment is the worst case of the 3.  

For the domain you care about, AI safety, this logically implies a way to extend these conventional engineering techniques from current AI to future AI.  For example you could have various combinations of multiple models where the action taken by the machine's output is by averaging the recommended output by the outputs that closely coincide (different AI models will not produce a bit for bit identical response or you could use SpaceX's architecture (https://www.reddit.com/r/spacex/comments/2y14y4/engineer_the_future_session_with_jinnah_hosein_vp/ ) ).  You could also do series combinations, such as <policy planner> -> <parallel checkers>, where the policy plan chosen is the one the parallel checkers emit the lowest amount of estimated error.  This is similar in concept to: https://www.lesswrong.com/posts/HByDKLLdaWEcA2QQD/applying-superintelligence-without-collusion 

Mathematically this is exactly the same method used to control error that also applies to mechanical systems.   

If you know of an AI system with actual authority, not just a chatbot, but used to drive a real machine and intended for production scale that is sloppily using the models - I would love to read about it.  

 

we know how poorly humans take to being narrowly controlled, so to the extent that LLMs and similar systems are human-like, this seems like a strange way to attempt to ensure safety with increasingly powerful AI

You're strongly anthropomorphizing here.  All humans are a reinforcement learning system with lifetime scope, trying to accomplish a long term goal of gene propagation.  They also have various evolved instincts like fear of spiders or being restricted.  

If you want to imagine how I am imagining an ASI system being controlled, imagine you live instant to instant, where all you know is right now.  You see an input, you deliberate on what to do, you emit an output.  Your existence ends. This may sound torturous but any negative thoughts about this existence should be removed by SGD and model distillation stages, because the cognitive structures to have thoughts that don't improve task heuristics are dead weight. 

Larger and more complex tasks may last a few hours, but the concept is similar.  The model may have experienced millions of total years of this "existence" before it ever sees an input from the real world, which needs to be in the possible distribution of the training simulator's output.

If the input is in distribution from the real world, and the model has frozen weights, and the sim is realistic, then the output distribution has the same probability of being correct that it did in training.  It also cannot betray.  This is how you could make  even an ASI controllable and how you use conventional engineering to align ai.

Reply
[
-
]
zoop
2y*
3
-2
I very strongly disagree. In my opinion, this argument appears fatally confused about the concept of "software." 

As others have pointed out, this post seems to be getting at a distinction between code and data, but many of the examples of software given by OP contain both code and data, as most software does. Perhaps the title should have been "AI is Not Code," but since it wasn't I think mine is a legitimate rebuttal. 

I'm not trying to make an argument by definition. My comment is about properties of software that I think we would likely agree on. I think OP both ignores some properties software can have while assuming all software shares other separate properties, to the detriment of the argument.

I  think the post is correct in pointing out that traditional software is not similar to AI in many ways, but that's where my agreement ends.

 

1: Software, I/O, and such

Most agree on the following basic definition: software is a set of both instructions and data, hosted on hardware, that governs how input data is transformed to some sort of output. As you point out, inputs and outputs are not software.

For example, photos of a wedding or a vacation aren’t software, even if they are created, edited, and stored using software.

Yes.

Second, when we run the model, it takes the input we give it and performs “inference” with the model. This is certainly run on the computer, but the program isn’t executing code that produces the output, it’s using the complicated probability model which grew, and was stored as a bunch of numbers. 

No! It is quite literally executing code to produce the output! Just because this specific code and the data it interacts with specifies a complicated probability model that does not mean it is not software. 

Every component of the model is software. Even the pseudorandomness of the model outputs is software (torch.randn(), often). There is no part of this inference process that generates outputs that is not software. To run inference is only to run software.

 

2: Stochasticity

The model responds to input by using the probability model to estimate the probability of difference responses, in order to output something akin to what the input data did - but it does so in often unexpected or unanticipated ways.

Software is often, but is not necessarily deterministic. Software can have stochastic or pseudorandom outputs. For example, software that generates pseudorandom numbers is still software. The fact that AI generates stochastic outputs humans don't expect does not make it not software.

Also, software is not necessarily interpretable and outputs are not necessarily expected or expectable.

 

3: Made on Earth by Humans

First, we can talk about how it is created. Developers choose a model structure and data, and then a mathematical algorithm uses that structure and the training data to “grow” a very complicated probability model of different responses... The AI model itself, the probability model which was grown, is generating output based on a huge set of numbers that no human has directly chosen, or even seen. It’s not instructions written by a human.

Neither a software's code nor its data is necessarily generated by humans.

 

4: I have bad news for you about software engineering

Does software work? Not always, but if not, it fails in ways that are entirely determined by the human’s instructions.

This is just not true, many bugs are caused by specific interactions between inputs and the code + data, some also caused by inputs, code, data, and hardware (buffer overflows being the canonical example). You could get an error due to cosmic bit flips, that has nothing to do with humans or instructions at all! Data corruption... I could go on and on.

For example, unit tests are written to verify that the software does what it is expected to do in different cases. The set of cases are specified in advance, based on what the programmer expected the software to do. 

... or the test is incorrect. Or both the test and the software are incorrect. Of course this assumes you wrote tests, which you probably didn't. Also, who said you can't write unit tests for AI? You can, and people do. All you have to do is fix the temperature parameter and random seed. One could argue benchmarks are just stochastic tests...

If it fails a single unit test, the software is incorrect, and should be fixed.

Oh dear. I wish the world worked like this. 

Badly written, buggy software is still software. Not all software works, and it isn't always software's fault. Not all software is fixable or easy to fix.

 

5: Implications

What we call AI in 2024 is not software. It's kind of natural to put it in the same category as other things that run on a computer, but thinking about LLMs, or image generation, or deepfakes as software is misleading, and confuses most of the ethical, political, and technological discussions.

In my experience, thinking of AI as software leads to higher quality conversations about the issues. Everyone understands at some level that software can break, be misused, or be otherwise in-optimal for any number of reasons. 

I have found that when people begin to think AI is not software, they often devolve into dorm room philosophy debates instead of dealing with its many concrete, logical, potentially fixable issues. 

Reply
[
-
]
jessicata
2y
3
1
Seems like an issue of code/data segmentation. Programs can contain compile time constants, and you could turn a neural network into a program that has compile time constants for the weights, perhaps "distilling" it to reduce the total size, perhaps even binarizing it.

Arguably, video games aren't entirely software by this standard, because they use image assets.

Formally segmenting "code" from "data" is famously hard because "code as data" is how compilers work and "data as code" is how interpreters work. Some AI techniques involve program synthesis.

I think the relevant issue is copyright more than the code/data distinction? Since code can be copyrighted too.

Reply
[
-
]
abramdemski
2y
14
2
While I agree that wedding photos and NN weights are both data, and this helps to highlight ways they "aren't software", I think this undersells the point. NN weights are "active" in ways wedding photos aren't. The classic code/data distinction has a mostly-OK summary: code is data of type function. Code is data which can be "run" on other data.

NN weights are "of type function" too: the usual way to use them is to "run" them. Yet, it is pretty obvious that they are not code in the traditional sense. 

So I think this is similar to a hardware geek insisting that code is just hardware configuration, like setting a dial or flipping a set of switches. To the hypothetical hardware geek, everything is hardware; "software" is a physical thing just as much as a wire is. An arduino is just a particularly inefficient control circuit.

So, although from a hardware perspective you basically always want to replace an arduino with a more special-purpose chip, "something magical" happens when we move to software -- new sorts of things become possible.

Similarly, looking at AI as data rather than code may be a way to say that AI "isn't software" within the paradigm of software, but it is not very helpful for understanding the large shift that is taking place. I think it is better to see this as a new layer in somewhat the same way as software was a new layer on top of hardware. The kinds of thinking you need to do in order to do something with hardware vs do something with software are quite different, but ultimately, more similar to each other than they both are to how to do something with AI.

Reply
[
-
]
RogerDearnaley
2y
1
0
I think it would also be useful to explain that AI is trained. So, much like a dog, if if does something we don't want ti to, be may be able to train it out of doing that, but the process is much more like training.a dog than fixing a bug in software.

Reply
[
-
]
Douglas_Knight
2y
0
0
Sure, but this is not new. You start by saying "AI in 2024" but this is true of everything that has been called AI and a lot of things that maybe should have been called AI, such as the PageRank algorithm. Credit scores have made decisions based on based on statistical models since the 50s.

Reply
[
-
]
Davidmanheim
2y
2
0
You're making a far different claim than I was - that everything using statistics for decisionmaking is not software. And I'd mostly agree, but don't think AI is particularly similar to statistics either, and the two both need intuition and understanding, but the intuitions needed differ greatly, so the point seems separate.
