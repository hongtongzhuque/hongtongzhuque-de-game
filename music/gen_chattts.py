import ChatTTS
import torch
import torchaudio
import os
from modelscope import snapshot_download

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("正在从 ModelScope 下载 ChatTTS 模型...")
model_dir = snapshot_download("pzc163/chatTTS")
print(f"模型路径: {model_dir}")

print("正在加载 ChatTTS...")
chat = ChatTTS.Chat()
chat.load(source="custom", custom_path=model_dir, compile=False)

print("正在合成遗书音频...\n")

texts = [
    "哥哥：写这封信的时候，窗外在下雨。我一直在想，如果雨停了，我是不是也能停下来。",
    "你还记得吗？小时候你送我的第一把小提琴。你说它旧了点，琴弦也有点松，但是声音很好听。我拉的第一首曲子叫《小星星》，拉得很难听，你在旁边笑得很大声，然后说：没关系，慢慢来。我一直在慢慢来。可是不知道为什么，她们觉得慢是一件很可笑的事。",
    "琴盒里第一次出现垃圾的时候，我以为是谁不小心放进去的。我倒了，擦了，第二天又是一盒。循环往复，像一首永远拉不完的练习曲。她们说，没有天赋的人不配碰音乐。她们说，你拉琴的声音像在杀鸡。她们说，你如果识相一点就该自己退社。我不知道识相是什么意思。我只是想和音符待在一起，只是想在下课后有一个可以去的地方。音乐从来没有嫌弃过我拉得不好，为什么人可以？",
    "后来我不拉琴了。那把旧小提琴一直放在柜子里，琴弦松了也没人调。我看着它，像看着一个死去的自己。哥哥，我知道你一定很生气。你一定想为我做些什么。但是答应我——不要变成和她们一样的人。不要让你的手沾上会让妈妈哭的东西。",
    "如果一定要有人记得我，就记得那个下午吧——我坐在窗边拉《小星星》，你在旁边笑，琴弦很松，声音很轻，但我们都很开心。晚是傍晚的晚。傍晚之后是夜晚，但夜晚之后，天会再亮。替我好好活着。替我把那首《小星星》拉完。周晚，于最后一个雨天的午后。",
]

params_infer_code = ChatTTS.Chat.InferCodeParams(
    temperature=0.3, top_P=0.7, top_K=20,
)
params_refine_text = ChatTTS.Chat.RefineTextParams(
    prompt="[oral_2][laugh_0][break_4]",
)

wavs = chat.infer(
    texts,
    params_refine_text=params_refine_text,
    params_infer_code=params_infer_code,
    use_decoder=True,
    skip_refine_text=False,
)

sample_rate = 24000
for i, wav in enumerate(wavs):
    filename = f"c{i+1}.wav"
    torchaudio.save(filename, torch.from_numpy(wav).unsqueeze(0), sample_rate)
    print(f"  -> {filename} ({len(wav)/sample_rate:.1f}秒)")

print(f"\n全部完成！文件：c1.wav ~ c5.wav")
