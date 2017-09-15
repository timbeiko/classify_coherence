# This is the script to run syntaxnet over the sentences. 
# In your syntaxnet installation (see https://github.com/tensorflow/models/tree/master/syntaxnet), 
# this script should be in the same directory as 'demo.sh' to run. 

# Also, you should add the following (uncommented) lines to context.pbtxt under /models/parsey_mcparseface
# input {
#   name: 'sentences'
#   record_format: 'english-text'
#   Part {
#     file_pattern: "PATH_TO_SENTENCE.txt"
#   }
# }

# input {
#   name: 'sentences-conll-temp'
#   record_format: 'conll-sentence'
#   Part {
#     file_pattern: "NEW_FILE_IN_SAME_DIRECTORY_AS_SENTENCE.txt"
#   }
# }

# input {
#   name: 'sentences-conll'
#   record_format: 'conll-sentence'
#   Part {
#     file_pattern: "PATH_TO_OUTPUT_SENTENCE.txt"
#   }
# }


PARSER_EVAL=bazel-bin/syntaxnet/parser_eval
MODEL_DIR=syntaxnet/models/parsey_mcparseface

# First parse the input with a tagger, and save the output to a temp file, 
# Then pipe the temp file through to the parser to generate the final conll output
$PARSER_EVAL \
  --input=sentences \
  --output=sentences-conll-temp \
  --model syntaxnet/models/parsey_mcparseface/tagger-params \
  --task_context syntaxnet/models/parsey_mcparseface/context.pbtxt \
  --hidden_layer_sizes 64 \
  --arg_prefix brain_tagger \
  --graph_builder structured \
  --slim_model \
  --batch_size 1024 | $PARSER_EVAL \
  --input sentences-conll-temp  \
  --output sentences-conll \
  --hidden_layer_sizes 512,512 \
  --arg_prefix brain_parser \
  --graph_builder structured \
  --task_context syntaxnet/models/parsey_mcparseface/context.pbtxt \
  --model_path syntaxnet/models/parsey_mcparseface/parser-params \
  --slim_model --batch_size 1024

