from transformers import AutoTokenizer, AutoModelWithLMHead
import random

tokenizer = AutoTokenizer.from_pretrained("cpierse/gpt2_film_scripts")
model = AutoModelWithLMHead.from_pretrained("cpierse/gpt2_film_scripts")
# making sure dropout is turned off
model.eval()
max_length = 1000
num_samples = 3

output = model.generate(
    bos_token_id=random.randint(1, 50000),
    do_sample=True,
    top_k=50,
    max_length=max_length,
    top_p=0.95,
    num_return_sequences=num_samples)

decoded_output = []
for sample in output:
    decoded_output.append(tokenizer.decode(
        sample, skip_special_tokens=True))
print(decoded_output[0])
