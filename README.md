# DeepGenome
Basis of the DeepGenome experiment

# Flow chart
1. **CalculateTotalSize Subgraph**:
- This subgraph represents the `calculate_total_size` function, which calculates the total size of a given shape.
- It starts by initializing the `total_size` variable to 1, then iterates through each dimension in the input shape, multiplying the `total_size` by the current dimension.
- Finally, it returns the calculated `total_size`.

2. **DeepDNAClass Subgraph**:
- This subgraph represents the `DeepDNA` class, which is the main class for the DNA generation and manipulation.
- It starts by initializing the class attributes, such as `inputs`, `outputs`, `flow`, and `operations`.
- It then defines the different operations (LINEAR, ADD, ASSIGNOUT) and their associated properties, including the `result_shape_of_tensor_sum` function for the ADD operation and the `opAssignOut_validation` function for the ASSIGNOUT operation.
- The class also includes methods for normalizing the inputs and outputs, generating the flow, optimizing the flow, merging with another flow, and printing the flow.

3. **DeepDNA_VarClass Subgraph**:
- This subgraph represents the `DeepDNA_Var` class, which is used to represent variables in the DNA flow.
- It initializes the attributes of the `DeepDNA_Var` class, including the `size` and `dependsOn` properties.

4. **DeepDNA_OperationClass Subgraph**:
- This subgraph represents the `DeepDNA_Operation` class, which is used to represent the different operations in the DNA flow.
- It initializes the attributes of the `DeepDNA_Operation` class, including the `name`, `numInputs`, `args`, and `validationFunc` properties.
- It also defines the `validation` method, which can be overridden by specific operation types.

5. **DeepDNA_SequenceClass Subgraph**:
- This subgraph represents the `DeepDNA_Sequence` class, which is used to represent a sequence of operations in the DNA flow.
- It initializes the attributes of the `DeepDNA_Sequence` class, including the reference to the `DeepDNA` instance, the `output`, `inputs`, `operation`, and `arguments`.
- It also includes the `choose` method, which is responsible for choosing the appropriate operation and inputs based on the available operations and variables.

6. **ExampleUsage Subgraph**:
- This subgraph represents the example usage of the `DeepDNA` class, including the creation of two DNA instances (DNA 1 and DNA 2), the generation and optimization of their flows, and the merging of the two flows into a new DNA instance.
- It demonstrates the step-by-step process of working with the `DeepDNA` class, including normalizing the inputs and outputs, generating the flow, optimizing the flow, and printing the flow for each DNA instance.
- Finally, it shows the merging of the two DNA flows into a new DNA instance and the printing of the merged flow.
