# Source Codes of Order Picker Routing Algorithm in A Rectangular Single-Block Warehouse   <br> 矩形单块仓库拣货路径规划算法源代码

:wave:
This repository contains the source Python codes used in the following paper:  
本项目包含的Python代码使用在以下论文中：
* Yuqi Liu, Haihui Shen, and Jun Xia (2024). [A more concise and efficient formulation of order picker routing in a rectangular single-block warehouse](https://doi.org/10.1109/IEEM62345.2024.10857038). *2024 IEEE International Conference on Industrial Engineering and Engineering Management (IEEM2024)*, 647-652. [[PDF](https://shenhaihui.github.io/research/papers/Routing_IEEM24.pdf)] [[errata](https://shenhaihui.github.io/research/papers/Routing_IEEM24_errata.pdf)]
  
and in the following master's thesis:  
以及下列硕士论文中：
* Yuqi Liu (2025). Re-Study of Picking Path Optimisation for Conventional Warehouses. Shanghai Jiao Tong University.  
  刘雨祺 (2025). 面向传统仓库的拣货路径优化再研究. 上海交通大学.

# Instruction 代码说明

* `DAP_algorithm.py`: Main codes of the DAP algorithm proposed in Liu et al. (2024). DAP算法运行代码。
* `PickingState.py` & `PickingInfo.py`: Required information of the DAP algorithm. DAP算法求解需要的信息。
* `RR_algorithm.py`: Main codes of the compared RR algorithm proposed in [Ratliff and Rosenthal (1983)](https://doi.org/10.1287/opre.31.3.507). RR算法运行代码。
* `Table1.xlsx` & `Table2.xlsx`：Required tables of the RR algorithm. RR算法所需的状态转移表。
* `\data`: contains the experiment instances, where 1-20 indicates the number of picking aisles, and for each number of picking aisles 100 instances are generated.
测试实例文件，1~20表示拣货巷道数量，每个拣货巷道数量下随机产生了100个实例。

# A Small Example 一个小例子

If you want to see a small example of the DAP algorithm, get into folder `\example` and run `DAP.py`, which will give you the following results:  
如果您想尝试使用DAP算法求解一个小例子，你可以进入`\example`文件夹，运行`DAP.py`，您将会得到以下结果：

![image](https://github.com/MyReStudy/single_block/blob/master/example/single_block_result.png)



# 论文引用说明
:star2:该项目相关论文链接：https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10857038

BibTeX引用格式：

```
@INPROCEEDINGS{10857038,
  author={Liu, Yuqi and Shen, Haihui and Xia, Jun},
  booktitle={2024 IEEE International Conference on Industrial Engineering and Engineering Management (IEEM)}, 
  title={A More Concise and Efficient Formulation of Order Picker Routing in a Rectangular Single-Block Warehouse}, 
  year={2024},
  pages={0647-0652},
  doi={10.1109/IEEM62345.2024.10857038}}
```

若您在后续研究或应用中使用到本项目涉及的思想与方法，请予以规范引用。

# 联系我
:blush:若您对本项目感兴趣，欢迎通过Github与我取得联系（或联系邮箱shenhaihui@sjtu.edu.cn；yuqi_liu@sjtu.edu.cn），期待与您交流探讨，共同推进仓库拣货路径规划算法研究进程。
