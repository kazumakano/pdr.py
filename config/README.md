# config
This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                   | Description                                                            | Notes                                    | Type          |
| ---                   | ---                                                                    | ---                                      | ---           |
| begin                 | begin datetime of RSSI log                                             | must be like 'yyyy-mm-dd hh:mm:ss'       | `str`         |
| end                   | end datetime of RSSI log                                               | must be like 'yyyy-mm-dd hh:mm:ss'       | `str`         |
| log_file              | acceleration and angular velocity log file                             |                                          | `str`         |
| init_direct           | initial direction [degree]                                             |                                          | `float`       |
| init_pos              | initial position [pixel]                                               |                                          | `list[float]` |
| result_file_name      | file name of image and video                                           | auto generated if unspecified            | `str \| None` |
|                       |                                                                        |                                          |               |
| enable_clear_map      | clear map image at each step or not                                    |                                          | `bool`        |
| enable_save_img       | capture image or not                                                   |                                          | `bool`        |
| enable_save_video     | record video or not                                                    |                                          | `bool`        |
| frame_rate            | frame rate of video [FPS]                                              | synchronized with real speed if 0        | `float`       |
| map_conf_file         | map config file                                                        |                                          | `str`         |
| map_img_file          | map image file                                                         |                                          | `str`         |
|                       |                                                                        |                                          |               |
| truth_log_file        | ground truth position log file                                         | disabled if unspecified                  | `str \| None` |
|                       |                                                                        |                                          |               |
| gyro_drift            | drift value of gyroscope [degree/second]                               |                                          | `float`       |
| rotate_ax             | rotation axis in smartphones coordinate frame                          | 1: +x, 2: -x, 3: +y, 4: -y, 5: +z, 6: -z | `int`         |
|                       |                                                                        |                                          |               |
| default_speed         | default subject's speed [meter/second]                                 |                                          | `float`       |
| max_status_interval   | maximum interval of status transitions to recognize as moving [second] |                                          | `float`       |
| min_step_interval     | minimum interval of steps to detect new one [second]                   |                                          | `float`       |
| stature               | subject's stature [meter]                                              |                                          | `float`       |
| step_len_coef         | ratio of step length to stature                                        |                                          | `float`       |
| step_begin_acc_thresh | threshold of acceleration for step bigin [G]                           |                                          | `float`       |
| pos_peak_acc_thresh   | threshold of acceleration for positive peak [G]                        |                                          | `float`       |
| neg_peak_acc_thresh   | threshold of acceleration for negative peak [G]                        |                                          | `float`       |
| step_end_acc_thresh   | threshold of acceleration for step end [G]                             |                                          | `float`       |
|                       |                                                                        |                                          |               |
| freq                  | frequency of inertial logs [Hz]                                        |                                          | `float`       |
| pdr_win_stride        | stride width of sliding window [second]                                | overlap is 0%, disabled if 0             | `float`       |
