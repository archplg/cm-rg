## How to read this network

Each circle is an LLM agent in the panel. Position on the canvas reflects how similarly the agent rated all the elements: agents close together reason about the decision in similar ways, agents far apart reason differently.

The lines between circles encode reasoning agreement. Green-and-thick = the two agents reason almost identically. Yellow-medium = they differ on framing. Red-thin = substantial disagreement at the reasoning level even if their final recommendations might match.

Inside each circle is the agent label and its epistemological frame (Quantitative, Systems, Engineering, Humanist, Contrarian). The halo color around each circle indicates which option that agent recommended.

For this case: **4/5 agents recommended option A with moderately different framings (RMSE=0.51). Worth probing what each is emphasizing.**

**Operator note:** the recommendation halos look unified (most agents chose the same option), but the network edges reveal underlying reasoning differences. Standard aggregation would miss this. Probe the framings before committing to execution.
