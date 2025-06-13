from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer
import os
import shutil

model_id = "gpt2"
onnx_dir = "./onnx/gpt2"

# 🔁 Step 1: Delete old export to avoid caching issues
if os.path.exists(onnx_dir):
    shutil.rmtree(onnx_dir)

# ✅ Step 2: Re-export GPT-2 to ONNX with use_cache=False and use_io_binding=False
model = ORTModelForCausalLM.from_pretrained(
    model_id,
    export=True,
    use_cache=False,         # 🧠 disables past_key_values
    use_io_binding=False     # ✅ REQUIRED to avoid conflict
)

# 💾 Step 3: Save the model and tokenizer
os.makedirs(onnx_dir, exist_ok=True)
model.save_pretrained(onnx_dir)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.save_pretrained(onnx_dir)

print(f"✅ Clean ONNX GPT-2 model exported to {onnx_dir}")