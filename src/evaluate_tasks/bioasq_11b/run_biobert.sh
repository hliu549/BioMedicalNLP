DATASET="BioAsq"
MODEL_DIR=model_dir/
# DATA_DIR=data_dir/
DATA_DIR=preprocessed_data/

BASE_MODEL="dmis-lab/biobert-v1.1"
MODEL="biobert-v1.1_SFull" \
# Ts=(-2 -3 -5 -10 -15 0.25 0.5 0.75 0.999)
Ts=(-10)
LR=1e-5
TRAIN_MODE="fusion"
for T in ${Ts[*]}; do
    python src/evaluate_tasks/bioasq_11b/eval_bioasq.py \
    --train_mode $TRAIN_MODE \
    --model_dir $MODEL_DIR \
    --data_dir $DATA_DIR  \
    --base_model $BASE_MODEL \
    --tokenizer $BASE_MODEL  \
    --model $MODEL  \
    --max_seq_length 512   \
    --batch_size 4 \
    --lr $LR   \
    --pretrain_epoch 0 \
    --epochs 10 \
    --temperature $T \
    --cuda \
    --inference_path temp/kg_infused_umls/
done