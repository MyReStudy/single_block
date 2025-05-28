# 单块仓库拣货路径规划算法

:wave:欢迎使用单块仓库拣货路径规划问题求解算法项目，该项目所属于毕业论文《面向传统仓库的拣货路径优化再研究》（2025.06），以及已发表论文A more concise and efficient formulation of order picker routing 
in a rectangular single-block warehouse。

# 快速体验

如果您想尝试求解小实验，可以进入example文件进行尝试，在该文件夹下为您提供了一个运行实例：

--test：一组测试数据

--DAP.py：程序入口，运行后得到规划结果如图

![image](https://github.com/MyReStudy/single_block/blob/master/example/single_block_result.png)

# 代码说明

--DAP_algorithm.py：DAP算法运行代码

--RR_algorithm.py：RR算法运行代码

--PickingState.py & PickingInfo.py：DAP的状态转移等求解需要的信息

--Table1.xlsx & Table2.xlsx：RR所需的状态转移表（与RR论文中一致）

--data：数据文件，1~20表示拣货巷道数量，不同拣货巷道下存储了100个实验数据

# 论文引用说明
该项目相关论文链接：https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10857038

BibTeX引用格式：
'''
@INPROCEEDINGS{10857038,
  author={Liu, Yuqi and Shen, Haihui and Xia, Jun},
  booktitle={2024 IEEE International Conference on Industrial Engineering and Engineering Management (IEEM)}, 
  title={A More Concise and Efficient Formulation of Order Picker Routing in a Rectangular Single-Block Warehouse}, 
  year={2024},
  pages={0647-0652},
  doi={10.1109/IEEM62345.2024.10857038}}
'''

若您在后续研究或应用中使用到本项目涉及的思想与方法，请予以规范引用。

# 联系我
:blush:若您对本项目感兴趣，欢迎通过Github与我取得联系（或联系邮箱shenhaihui@sjtu.edu.cn；yuqi_liu@sjtu.edu.cn），期待与您交流探讨，共同推进仓库拣货路径规划算法研究。
