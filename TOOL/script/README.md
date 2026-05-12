# TOOL 脚本说明

这些脚本用于本地音频转文本流程：

1. 把长 MP3 切分成较短音频片段。
2. 必要时把本地音频上传到七牛 Kodo。
3. 调用 QNAIGC ASR，生成转写文本和原始响应 JSON。

建议所有命令都从仓库根目录运行：

```bash
cd /Users/mac/studyspace/algo-engineer-os
```

## 环境准备

使用 conda 创建环境：

```bash
conda env create -f TOOL/script/environment.yml
conda activate audio2text-asr
```

或者在已有 Python 环境中安装依赖：

```bash
python -m pip install -r TOOL/script/requirements.txt
```

创建本地配置文件：

```bash
cp TOOL/script/.env.example TOOL/script/.env
```

然后填写 `TOOL/script/.env`。

ASR 必填：

```bash
QNAIGC_API_KEY=<API_KEY>
```

ASR 需要拿到可访问的音频 URL，二选一：

```bash
# 方案 A：TOOL/audios 里的文件已经可以通过下面形式访问：
# ${QNAIGC_AUDIO_BASE_URL}/${filename}
QNAIGC_AUDIO_BASE_URL=

# 方案 B：先把本地音频上传到七牛 Kodo，再把上传后的 URL 交给 ASR。
QINIU_ACCESS_KEY=
QINIU_SECRET_KEY=
QINIU_BUCKET=
QINIU_DOMAIN=
QINIU_KEY_PREFIX=asr-audios
QINIU_PRIVATE_BUCKET=false
QINIU_UPLOAD_TOKEN_EXPIRES=3600
```

`TOOL/script/.env` 已经被 Git 忽略，不会提交到仓库。

## 目录依赖

脚本默认路径是根据脚本自身位置推导出来的：

| 脚本 | 默认输入 | 默认输出 |
| --- | --- | --- |
| `split_mp3.py` | `TOOL/audios/aiops_extracted.mp3` | `TOOL/audio_chunks/` |
| `upload_to_kodo.py` | `TOOL/audios/` | `TOOL/kodo_uploads.json` |
| `audio2text.py` | `TOOL/audios/` | `TOOL/transcripts/` |

注意：如果你手动传入路径参数，例如 `--input-dir audio_chunks_300`，这个相对路径会按当前运行命令的目录解析，而不是按 `TOOL/script` 解析。因此建议从仓库根目录运行，或者显式写成 `TOOL/audio_chunks_300`。

`.env` 查找顺序：

1. 如果传了 `--env <path>`，优先使用这个路径。
2. 当前运行目录下的 `.env`。
3. `TOOL/script/.env`。
4. 仓库根目录下的 `.env`。

`TOOL/` 下的生成文件默认都被 Git 忽略，只有 `TOOL/script/**` 会保留在 Git 变更里。

## 切分 MP3

把默认 MP3 切成 300 秒片段：

```bash
python TOOL/script/split_mp3.py
```

等价的显式命令：

```bash
python TOOL/script/split_mp3.py \
  --input TOOL/audios/aiops_extracted.mp3 \
  --output-dir TOOL/audio_chunks \
  --chunk-seconds 300
```

切到已有的 300 秒片段目录：

```bash
python TOOL/script/split_mp3.py \
  --input TOOL/audios/aiops_extracted.mp3 \
  --output-dir TOOL/audio_chunks_300 \
  --chunk-seconds 300
```

只生成第一个片段，用于快速测试：

```bash
python TOOL/script/split_mp3.py \
  --input TOOL/audios/aiops_extracted.mp3 \
  --output-dir TOOL/audio_chunks \
  --chunk-seconds 300 \
  --limit 1
```

## 上传到七牛 Kodo

只检查默认 `TOOL/audios/` 目录的上传计划，不实际上传：

```bash
python TOOL/script/upload_to_kodo.py --dry-run
```

上传 `TOOL/audios/` 里的所有音频，并写出 `TOOL/kodo_uploads.json`：

```bash
python TOOL/script/upload_to_kodo.py
```

上传切分后的音频目录，并写出单独的 manifest：

```bash
python TOOL/script/upload_to_kodo.py \
  --input TOOL/audio_chunks_300 \
  --manifest TOOL/kodo_uploads_chunks_300.json
```

只上传单个文件：

```bash
python TOOL/script/upload_to_kodo.py \
  --input TOOL/audios/aiops_extracted.mp3
```

覆盖 Kodo 中同 key 的已有对象：

```bash
python TOOL/script/upload_to_kodo.py \
  --input TOOL/audio_chunks_300 \
  --overwrite
```

指定 env 文件：

```bash
python TOOL/script/upload_to_kodo.py \
  --env TOOL/script/.env \
  --input TOOL/audio_chunks_300
```

## 调用 ASR 转写

只检查 ASR 配置和音频 URL 解析，不实际调用 ASR：

```bash
python TOOL/script/audio2text.py --dry-run
```

转写默认输入目录，输出到默认目录：

```bash
python TOOL/script/audio2text.py
```

转写切分后的音频，并输出到已有的 chunk 转写目录：

```bash
python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300
```

如果 `QNAIGC_AUDIO_BASE_URL` 为空，则先把每个本地音频上传到 Kodo，再调用 ASR：

```bash
python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300 \
  --upload
```

即使 `.txt` 输出已经存在，也强制重新转写：

```bash
python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300 \
  --force
```

只处理第一个文件，用于快速测试：

```bash
python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300 \
  --limit 1
```

增加单个音频的 ASR HTTP 超时时间：

```bash
python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300 \
  --timeout 300
```

## 常见流程

先切分长 MP3，再通过公网 base URL 转写：

```bash
python TOOL/script/split_mp3.py \
  --input TOOL/audios/aiops_extracted.mp3 \
  --output-dir TOOL/audio_chunks_300 \
  --chunk-seconds 300

python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300
```

先切分长 MP3，再上传 Kodo，然后转写：

```bash
python TOOL/script/split_mp3.py \
  --input TOOL/audios/aiops_extracted.mp3 \
  --output-dir TOOL/audio_chunks_300 \
  --chunk-seconds 300

python TOOL/script/upload_to_kodo.py \
  --input TOOL/audio_chunks_300 \
  --manifest TOOL/kodo_uploads_chunks_300.json

python TOOL/script/audio2text.py \
  --input-dir TOOL/audio_chunks_300 \
  --output-dir TOOL/transcripts_chunks_300 \
  --upload
```

## 输出说明

`audio2text.py` 会为每个输入音频写两个文件：

```text
TOOL/transcripts*/<audio_stem>.json
TOOL/transcripts*/<audio_stem>.txt
```

`.json` 是 ASR 原始响应。`.txt` 是脚本从响应中提取出来的转写文本；如果没有找到明显的文本字段，就会把格式化后的 JSON 写入 `.txt`。

