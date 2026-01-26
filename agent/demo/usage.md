# 生成索引文件
```bash
# 创建文档
python create_index_sample.py

# 构建知识库（向量）
python main.py build sample_intel_manual.txt --type both

# 查询
python main.py query "What is the MOV instruction?"
```

# 运行主程序
```bash
# Interactive mode (default)
python main.py

# Run the sample task (analyze week1/week2 projects)
python main.py --mode sample

# Execute a single task from command line
python main.py --mode single --task "Create a hello world Python script"

# Run demonstrations
python main.py --mode demo --demo basic
python main.py --mode demo --demo loop
python main.py --mode demo --demo comparison

# Disable specific features
python main.py --no-todo --no-timestamps --task "Simple task"

# Quick start with sample task
python quickstart.py

# View saved trajectory after running any task
python view_trajectory.py

# View a specific trajectory file
python view_trajectory.py path/to/trajectory.json
```