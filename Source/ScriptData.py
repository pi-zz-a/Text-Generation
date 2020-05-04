# Thanks to the team at huggingface for providing their example
# on fine_tuning a dataset, this dataset class borrows heavily from that it.
# Find a link to their example below
# https://github.com/huggingface/transformers/blob/master/examples/run_language_modeling.py


class ScriptData(Dataset):
    def __init__(
            self,
            tokenizer: PreTrainedTokenizer,
            file_path: str,
            block_size=512,
            overwrite_cache=False,
    ):
        assert os.path.isfile(file_path)

        block_size = block_size - (
                tokenizer.max_len - tokenizer.max_len_single_sentence
        )

        directory, filename = os.path.split(file_path)

        # change if args are added at later point
        cached_features_file = os.path.join(
            directory, "gpt2" + "_" + str(block_size) + "_" + filename
        )

        if os.path.exists(cached_features_file) and not overwrite_cache:
            logger.info(
                f"Loading features from your cached file {cached_features_file}"
            )
            with open(cached_features_file, "rb") as cache:
                self.examples = pickle.load(cache)
                logger.debug("Loaded examples from cache")
        else:
            logger.info(f"Creating features from file {filename} at {directory}")

            self.examples = []
            with open(file_path, encoding="utf-8") as f:
                text = f.read()
                logger.debug("Succesfully read text from file")

            tokenized_text = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text))

            for i in range(0, len(tokenized_text) - block_size + 1, block_size):
                self.examples.append(
                    tokenizer.build_inputs_with_special_tokens(
                        tokenized_text[i: i + block_size]
                    )
                )

            logger.info(f"Saving features into cached file {cached_features_file}")
            with open(cached_features_file, "wb") as cache:

                pickle.dump(self.examples, cache, protocol=pickle.HIGHEST_PROTOCOL)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        return torch.tensor(self.examples[item], dtype=torch.long)