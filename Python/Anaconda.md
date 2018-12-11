# Anaconda

## 虚拟环境

```sh
# 列出所有虚拟环境
$ conda env list
$ conda-env list

$ conda create -n env_name python=x.x  # 创建虚拟环境
$ conda remove -n env_name --all  # 移除虚拟环境
$ conda activate env_name  # 使用虚拟环境
$ conda deactivate env_name  # 退出虚拟环境
```

虚拟环境的所有相关文件都在anaconda/envs目录下