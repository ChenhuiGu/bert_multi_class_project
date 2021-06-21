
from simpletransformers.classification import ClassificationModel, ClassificationArgs
from config import num_train_epochs, learning_rate, train_batch_size, \
    eval_batch_size, max_seq_length, output_path
from data.multi_class_example import loan_usage_example, split_example_KFold, get_label_map
from utils.srf_log import logger


class BertmultiClass():
    def __init__(self):
        # Optional model configuration
        self.model_args = ClassificationArgs(num_train_epochs=num_train_epochs,
                                             learning_rate=learning_rate,
                                             train_batch_size=train_batch_size,
                                             eval_batch_size=eval_batch_size,
                                             max_seq_length=max_seq_length,
                                             output_dir=output_path
                                             )
        # self.cuda_available = torch.cuda.is_available()

    def train(self):
        df = loan_usage_example()
        label_map = get_label_map()
        train_df, eval_df = split_example_KFold(df)
        # Create a ClassificationModel
        model = ClassificationModel(
            'bert',
            'hfl/chinese-bert-wwm-ext',
            num_labels=len(label_map),
            args=self.model_args,
            # use_cuda=self.cuda_available
            use_cuda=True
        )
        # Train the model
        model.train_model(train_df)

        # Evaluate the model
        result, model_outputs, wrong_predictions = model.eval_model(eval_df)
        logger.info(f'Evaluate the model:result:{result}\n,wrong_predictions:{wrong_predictions}')

    def predict(self, text):
        label_map = get_label_map()
        model = ClassificationModel(
            'bert',
            f'{output_path}/best_mode',
            num_labels=len(label_map),
            args=self.model_args,
            # use_cuda=self.cuda_available
            use_cuda=True
        )
        # Make predictions with the model
        predictions, raw_outputs = model.predict([text])
        return predictions


if __name__ == '__main__':
    model = BertmultiClass()
    model.train()