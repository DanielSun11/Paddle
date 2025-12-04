# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def sum_ranges(ranges):
    result = 0
    for time_range in ranges:
        result += time_range[1] - time_range[0]
    return result


def merge_self_ranges(src_ranges, is_sorted=False):
    merged_ranges = []
    if len(src_ranges) > 0:
        if not is_sorted:
            src_ranges.sort(key=lambda x: x[0])
        cur_index = 0
        merged_ranges.append(
            (src_ranges[cur_index][0], src_ranges[cur_index][1])
        )
        for cur_index in range(1, len(src_ranges)):
            if src_ranges[cur_index][1] > merged_ranges[-1][1]:
                if src_ranges[cur_index][0] <= merged_ranges[-1][1]:
                    merged_ranges[-1] = (
                        merged_ranges[-1][0],
                        src_ranges[cur_index][1],
                    )
                else:
                    merged_ranges.append(
                        (src_ranges[cur_index][0], src_ranges[cur_index][1])
                    )
    return merged_ranges


def merge_ranges(range_list1, range_list2, is_sorted=False):
    merged_ranges = []
    if not is_sorted:
        range_list1 = merge_self_ranges(range_list1)
        range_list2 = merge_self_ranges(range_list2)
    len1 = len(range_list1)
    len2 = len(range_list2)
    if len1 == 0 and len2 == 0:
        return merged_ranges
    elif len1 == 0:
        return range_list2
    elif len2 == 0:
        return range_list1
    else:
        index1 = 0
        index2 = 0
        range1 = range_list1[index1]
        range2 = range_list2[index2]
        if range1[0] < range2[0]:
            merged_ranges.append(range1)
            index1 += 1
        else:
            merged_ranges.append(range2)
            index2 += 1
        while index1 < len1 and index2 < len2:
            range1 = range_list1[index1]
            range2 = range_list2[index2]
            if range1[0] < range2[0]:
                if range1[1] > merged_ranges[-1][1]:
                    if range1[0] <= merged_ranges[-1][1]:
                        merged_ranges[-1] = (merged_ranges[-1][0], range1[1])
                    else:
                        merged_ranges.append((range1[0], range1[1]))
                    index1 += 1
                else:
                    index1 += 1
            else:
                if range2[1] > merged_ranges[-1][1]:
                    if range2[0] <= merged_ranges[-1][1]:
                        merged_ranges[-1] = (merged_ranges[-1][0], range2[1])
                    else:
                        merged_ranges.append((range2[0], range2[1]))
                    index2 += 1
                else:
                    index2 += 1

        while index1 < len1:
            range1 = range_list1[index1]
            if range1[1] > merged_ranges[-1][1]:
                if range1[0] <= merged_ranges[-1][1]:
                    merged_ranges[-1] = (merged_ranges[-1][0], range1[1])
                else:
                    merged_ranges.append((range1[0], range1[1]))
                index1 += 1
            else:
                index1 += 1
        while index2 < len2:
            range2 = range_list2[index2]
            if range2[1] > merged_ranges[-1][1]:
                if range2[0] <= merged_ranges[-1][1]:
                    merged_ranges[-1] = (merged_ranges[-1][0], range2[1])
                else:
                    merged_ranges.append((range2[0], range2[1]))
                index2 += 1
            else:
                index2 += 1
    return merged_ranges


def intersection_ranges(range_list1, range_list2, is_sorted=False):
    result_range = []
    if len(range_list1) == 0 or len(range_list2) == 0:
        return result_range
    if not is_sorted:
        range_list1 = merge_self_ranges(range_list1)
        range_list2 = merge_self_ranges(range_list2)

    len1 = len(range_list1)
    len2 = len(range_list2)
    index1 = 0
    index2 = 0
    range1 = range_list1[index1]
    range2 = range_list2[index2]
    while index1 < len1 and index2 < len2:
        if range2[1] <= range1[0]:
            index2 += 1
            if index2 == len2:
                break
            range2 = range_list2[index2]

        elif range2[0] <= range1[0] and range2[1] < range1[1]:
            assert range2[1] > range1[0]
            result_range.append((range1[0], range2[1]))
            range1 = (range2[1], range1[1])
            index2 += 1
            if index2 == len2:
                break
            range2 = range_list2[index2]

        elif range2[0] <= range1[0]:
            assert range2[1] >= range1[1]
            result_range.append(range1)
            range2 = (range1[1], range2[1])
            index1 += 1
            if index1 == len1:
                break
            range1 = range_list1[index1]

        elif range2[1] < range1[1]:
            assert range2[0] > range1[0]
            result_range.append(range2)
            range1 = (range2[1], range1[1])
            index2 += 1
            if index2 == len2:
                break
            range2 = range_list2[index2]

        elif range2[0] < range1[1]:
            assert range2[1] >= range1[1]
            result_range.append((range2[0], range1[1]))
            range2 = (range1[1], range2[1])
            index1 += 1
            if index1 == len1:
                break
            range1 = range_list1[index1]

        else:
            assert range2[0] >= range1[1]
            index1 += 1
            if index1 == len1:
                break
            range1 = range_list1[index1]
    return result_range


def subtract_ranges(range_list1, range_list2, is_sorted=False):
    result_range = []
    if not is_sorted:
        range_list1 = merge_self_ranges(range_list1)
        range_list2 = merge_self_ranges(range_list2)
    if len(range_list1) == 0:
        return result_range
    if len(range_list2) == 0:
        return range_list1

    len1 = len(range_list1)
    len2 = len(range_list2)
    index1 = 0
    index2 = 0
    range1 = range_list1[index1]
    range2 = range_list2[index2]

    while index1 < len(range_list1):
        if index2 == len(range_list2):
            result_range.append(range1)
            index1 += 1
            if index1 == len1:
                break
            range1 = range_list1[index1]
        elif range2[1] <= range1[0]:
            index2 += 1
            if index2 != len2:
                range2 = range_list2[index2]
        elif range2[0] <= range1[0] and range2[1] < range1[1]:
            range1 = (range2[1], range1[1])
            index2 += 1
            if index2 != len2:
                range2 = range_list2[index2]
        elif range2[0] <= range1[0]:
            assert range2[1] >= range1[1]
            range2 = (range1[1], range2[1])
            index1 += 1
            if index1 != len1:
                range1 = range_list1[index1]
        elif range2[0] < range1[1]:
            assert range2[0] > range1[0]
            result_range.append((range1[0], range2[0]))
            range1 = (range2[0], range1[1])
        else:
            assert range2[0] >= range1[1]
            result_range.append(range1)
            index1 += 1
            if index1 != len1:
                range1 = range_list1[index1]
    return result_range


class DistributeGPUTimeCollector:
    op_gpu_time = {}
    gathered_op_gpu_time = {}
    need_collect = False

    @classmethod
    def enable_collect(cls):
        cls.need_collect = True

    @classmethod
    def disable_collect(cls):
        cls.need_collect = False

    @classmethod
    def add_into_gpu_times(cls, op_name, call, gpu_time):
        if op_name not in cls.op_gpu_time:
            cls.op_gpu_time[op_name] = [0, 0]
        cls.op_gpu_time[op_name][0] += call
        cls.op_gpu_time[op_name][1] += gpu_time

    @classmethod
    def try_collect(cls, items):
        if not cls.need_collect:
            return

        for key in items.keys():
            op_item = items[key]
            # Remove the  duplicated statistic op in pylayer backward
            if "GradNodePyLayer" in key or "GradNodeAccumulation" in key:
                for (
                    innerop_name,
                    innerop_node,
                ) in op_item.operator_inners.items():
                    if "pybind_imperative_func" in innerop_name:
                        op_item.cpu_time = (
                            op_item.cpu_time - innerop_node.cpu_time
                        )
                        op_item.general_gpu_time = (
                            op_item.general_gpu_time
                            - innerop_node.general_gpu_time
                        )
                    elif innerop_node.general_gpu_time > 0:
                        cls.add_into_gpu_times(
                            innerop_name,
                            innerop_node.call,
                            innerop_node.general_gpu_time,
                        )
                for name, device_node in op_item.devices.items():
                    cls.add_into_gpu_times(
                        device_node.name, device_node.call, device_node.gpu_time
                    )
            elif op_item.general_gpu_time > 0:
                cls.add_into_gpu_times(
                    key, op_item.call, op_item.general_gpu_time
                )
        print(cls.op_gpu_time)

    @classmethod
    def aggregate_from_distribute_workers(cls):
        import paddle.distributed as dist

        group = dist.collective._get_global_group()
        all_workers_gpu_time = []
        dist.all_gather_object(all_workers_gpu_time, cls.op_gpu_time)

        def aggregate_gpu_time(all_workers_gpu_time):
            aggregated_gpu_time = {}
            for d in all_workers_gpu_time:
                for key, values in d.items():
                    if key not in aggregated_gpu_time:
                        aggregated_gpu_time[key] = [0] * len(values)
                    aggregated_gpu_time[key] = [
                        sum_val + val
                        for sum_val, val in zip(
                            aggregated_gpu_time[key], values
                        )
                    ]
            return aggregated_gpu_time

        cls.gathered_op_gpu_time = aggregate_gpu_time(all_workers_gpu_time)

    @classmethod
    def show_result(cls):
        sorted_by_value_desc = dict(
            sorted(
                cls.gathered_op_gpu_time.items(),
                key=lambda item: item[1][1],
                reverse=True,
            )
        )
        for op_name, item in sorted_by_value_desc.items():
            time = float(item[1]) / 1000000
            max_length = 50
            print(
                f"{op_name if len(op_name) <= max_length else op_name[: max_length - 3] + '...'} |{item[0]} |{time:.3f}"
            )
