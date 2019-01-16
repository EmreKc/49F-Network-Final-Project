from operator import attrgetter
import time
import random
import math

import machine
import video
import channel

start_time = time.time()
machines = []
videosBase = []
videosEnhancement = []
dist_machines = []
baseX = 300
baseY = 300
where_base = int
where_enhancement = int
ordered_machines = []
channels = []
channels_history = []

channel_no = 702

for i in range(9):
    c = channel.Channel()
    ch = channel.ChannelHistory()
    c.c_id, ch.c_id = channel_no, channel_no
    channel_no += 2
    c.availability = random.randint(0, 1)
    channels.append(c)
    channels_history.append(ch)

while len(machines) < 500:
    include = False
    machineX = random.randint(0, 600)
    machineY = random.randint(0, 600)
    ax = (baseX - machineX) ** 2
    ay = (baseY - machineY) ** 2
    distance = math.sqrt(ax + ay)
    if distance < 300:
        new_machine = machine.Machine()
        new_machine.x = machineX
        new_machine.y = machineY
        for m in machines:
            if machineX == m.x and machineY == m.y:
                include = True
        if include is False:
            new_machine.m_id = len(machines) + 1
            new_machine.channel = 702 if new_machine.m_id % 9 is 0 else 704 if new_machine.m_id % 9 is 1 else 706 if new_machine.m_id % 9 is 2 else 708 \
                if new_machine.m_id % 9 is 3 else 710 if new_machine.m_id % 9 is 4 else 712 if new_machine.m_id % 9 is 5 else 714 if new_machine.m_id % 9 is 6 else 716 \
                if new_machine.m_id % 9 is 7 else 718
            machines.append(new_machine)

over = 0
for i in range(1, 101):
    over += 1 / (i ** 0.8)

for i in range(1, 101):
    vdB = video.VideoBase()
    vdE = video.VideoEnhancement()
    vdB.v_id = i
    vdE.v_id = i
    a = (1 / i ** 0.8) / over
    vdB.popularity, vdE.popularity = a, a
    videosBase.append(vdB)
    videosEnhancement.append(vdE)

temp_machines = machines.copy()
while temp_machines:  # distribute videos to machines' caches
    num = random.randint(0, len(temp_machines) - 1)
    videos_base = videosBase.copy()
    videos_enhancement = videosEnhancement.copy()
    cont_list = []
    while temp_machines[num].cache_size < 1000:

        len1 = len(videos_base)
        random_number = random.randint(0, (len1 + len(videos_enhancement) - 1))
        if random_number < len1:
            v_id = videos_base[random_number].v_id
            layer_id = 0
            if (temp_machines[num].cache_size + (25 if layer_id == 0 else 5)) <= 1000:
                videos_base.remove(videos_base[random_number])
        else:
            v_id = videos_enhancement[random_number - len1].v_id
            layer_id = 1
            if (temp_machines[num].cache_size + (25 if layer_id == 0 else 5)) <= 1000:
                videos_enhancement.remove(videos_enhancement[random_number - len1])

        cont = machine.Content()
        cont.v_id = v_id
        cont.layer_id = layer_id
        if (temp_machines[num].cache_size + (25 if layer_id == 0 else 5)) <= 1000:
            cont_list.append(cont)
            temp_machines[num].cache_size += (25 if layer_id == 0 else 5)

    dist_machines.append(temp_machines[num])
    dist_machines[-1].contents = sorted(cont_list, key=attrgetter('v_id', 'layer_id'))
    temp_machines.remove(temp_machines[num])


# simulation

def order_machines():
    currentX = dist_machines[random_machine].x
    currentY = dist_machines[random_machine].y
    distances = []
    sorted_machines = []
    for im in range(len(dist_machines)):
        bx = (currentX - dist_machines[im].x) ** 2
        by = (currentY - dist_machines[im].y) ** 2
        dist = math.sqrt(bx + by)
        d_dist = machine.Distance()
        d_dist.distance = dist
        d_dist.index = im
        distances.append(d_dist)
    sorted_distances = sorted(distances, key=attrgetter('distance'))
    for dm in sorted_distances:
        sorted_machines.append(dist_machines[dm.index])
    return sorted_machines


videoBase_founded = False
videoEnhancement_founded = False
videoEnhancement_founded_printed = False
videoBase_founded_printed = False
print('1) LRU')
print('2) LFU')
print('3) ARC')
while True:
    try:
        question = int(input('(1,2,3), which is your favourite algorithm?'))
        break
    except ValueError:
        print("That's not a valid option!")

for j in range(100):
    random_machine = random.randint(0, 499)  # select random machine
    random_video = random.randint(0, len(videosBase) + len(videosEnhancement) - 1)  # select random video in videosBase or VideosEnhancement
    if random_video < len(videosBase):
        selected_video = videosBase[random_video]
    else:
        selected_video = videosEnhancement[random_video - len(videosBase)]
    videoBase_founded = False
    videoEnhancement_founded = False
    videoEnhancement_founded_printed = False
    videoBase_founded_printed = False

    for c in dist_machines[random_machine].contents:  # if selected_video is in selected machine
        if (selected_video.v_id is c.v_id) and ((0 if selected_video.layer is 25 else 1) is c.layer_id):
            if selected_video.layer is 25:
                if videoBase_founded is False:
                    print(f"Video {selected_video.v_id} Base Found")
                    where_base = 0
                videoBase_founded = True
            elif selected_video.layer is 5:
                if videoEnhancement_founded is False:
                    print(f"Video {selected_video.v_id} Enhancement Found")
                    where_enhancement = 0
                videoEnhancement_founded = True
                base_video = videosBase[random_video - len(videosBase)]
                for ci in dist_machines[random_machine].contents:
                    if (base_video.v_id is ci.v_id) and (base_video.layer is 25):
                        if videoBase_founded is False:
                            print(f"Video {selected_video.v_id} Base Found")
                            where_base = 0
                        videoBase_founded = True
                        break
        if (selected_video.layer is 5) and videoBase_founded and videoEnhancement_founded:
            print(f"Video {selected_video.v_id} HQ founded")
            videoEnhancement_founded_printed = True
            break
        elif (selected_video.layer is 25) and videoBase_founded:
            print(f"Video {selected_video.v_id} SQ founded")
            videoBase_founded_printed = True
            break
    ordered_machines = order_machines()

    if not (((selected_video.layer is 5) and videoBase_founded and videoEnhancement_founded) or \
            ((selected_video.layer is 25) and videoBase_founded)):  # if video could not found in selected machine
        for sm in range(len(ordered_machines)):
            for c in ordered_machines[sm].contents:
                if (selected_video.v_id is c.v_id) and ((0 if selected_video.layer is 25 else 1) is c.layer_id):
                    if selected_video.layer is 25:
                        if videoBase_founded is False:
                            print(f"Video {selected_video.v_id} Base Found")
                            where_base = sm
                        videoBase_founded = True
                    elif selected_video.layer is 5:
                        if videoEnhancement_founded is False:
                            print(f"Video {selected_video.v_id} Enhancement Found")
                            where_enhancement = sm
                        videoEnhancement_founded = True
                        base_video = videosBase[random_video - len(videosBase)]
                        for ci in ordered_machines[sm].contents:
                            if (base_video.v_id is ci.v_id) and (base_video.layer is 25):
                                if videoBase_founded is False:
                                    print(f"Video {selected_video.v_id} Base Found")
                                    where_base = sm
                                videoBase_founded = True
                                break
                if (selected_video.layer is 5) and videoBase_founded and videoEnhancement_founded:
                    if videoEnhancement_founded_printed is False:
                        print(f"Video {selected_video.v_id} HQ founded")
                    videoEnhancement_founded_printed = True
                    break
                elif (selected_video.layer is 25) and videoBase_founded:
                    if videoBase_founded_printed is False:
                        print(f"Video {selected_video.v_id} SQ founded")
                    videoBase_founded_printed = True
                    break
            if (selected_video.layer is 5) and videoBase_founded and videoEnhancement_founded:
                if videoEnhancement_founded_printed is False:
                    print(f"Video {selected_video.v_id} HQ founded")
                break
            elif (selected_video.layer is 25) and videoBase_founded:
                if videoBase_founded_printed is False:
                    print(f"Video {selected_video.v_id} SQ founded")
                break
    if not (((selected_video.layer is 5) and videoBase_founded and videoEnhancement_founded) or ((selected_video.layer is 25) and videoBase_founded)):
        print("No such video in cache")

    if (selected_video.layer is 5) and videoBase_founded and videoEnhancement_founded:  # if HQ video founded
        print(f"Base Layer in {where_base} , Enhancement Layer in  {where_enhancement}")
        videoBase_sent = False
        videoEnhancement_sent = False
        for x in range(len(channels)):
            if channels[x].c_id is ordered_machines[where_base].channel and not videoBase_sent:  # get Base layer
                if channels[x].availability is 1:  # if channel is available
                    h = channel.History()
                    h.v_id = selected_video.v_id
                    h.layer = 25
                    channels_history[x].history_queue.put(h)
                    channels[x].availability = 0
                    videoBase_sent = True
                else:  # if channel  is not available
                    for nx in range(len(channels)):
                        if channels[nx].availability is 1 and not videoBase_sent:
                            channels[x].availability = 1
                            channels[nx].availability = 0
                            h = channel.History()
                            h.v_id = selected_video.v_id
                            h.layer = 25
                            channels_history[x].history_queue.put(h)
                            videoBase_sent = True

            if channels[x].c_id is ordered_machines[where_enhancement].channel and not videoEnhancement_sent:  # get Enhancement Layer
                if channels[x].availability is 1:  # if channel is available
                    h = channel.History()
                    h.v_id = selected_video.v_id
                    h.layer = 5
                    channels_history[x].history_queue.put(h)
                    channels[x].availability = 0
                    videoEnhancement_sent = True
                else:  # if channel  is not available
                    for nx in range(len(channels)):
                        if channels[nx].availability is 1 and not videoEnhancement_sent:
                            channels[x].availability = 1
                            channels[nx].availability = 0
                            h = channel.History()
                            h.v_id = selected_video.v_id
                            h.layer = 5
                            channels_history[x].history_queue.put(h)
                            videoEnhancement_sent = True
        if question is 1:
            cache_videos = []
            for con in ordered_machines[0].contents:
                for vid in videosBase:
                    if con.v_id is vid.v_id and con.layer_id is 0:
                        cache_videos.append(vid)
                        break
                for vid in videosEnhancement:
                    if con.v_id is vid.v_id and con.layer_id is 1:
                        cache_videos.append(vid)
                        break
            tempBase_video = videosBase[random_video - len(videosBase)]
            tempEnchancement_video = videosEnhancement[random_video - len(videosBase)]
            temp_video = videosBase[random_video - len(videosBase)]
            firstBase_match = False
            firstEnhancement_match = False
            for x in range(len(cache_videos)):
                if not firstBase_match:
                    if cache_videos[x].layer is 25:
                        temp_video = cache_videos[x]
                        cache_videos[x] = tempBase_video
                        tempBase_video = temp_video
                        continue
                if not firstEnhancement_match:
                    if cache_videos[x].layer is 5:
                        temp_video = cache_videos[x]
                        cache_videos[x] = tempEnchancement_video
                        tempBase_video = temp_video
                        continue
                if cache_videos[x].v_id is videosBase[random_video - len(videosBase)].v_id:
                    cache_videos[x] = tempBase_video

                temp_video = cache_videos[x]
                cache_videos[x] = videosBase
                tempBase_video = temp_video
            for i in cache_videos:
                print(i)

        elif question is 2:
            cache_videos = []
            if where_base == 0:
                for con in ordered_machines[0].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
            else:
                for con in ordered_machines[0].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 25:
                            cache_videos.append(vid)

                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            cache_videos.append(vid)
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                for cn in cache_videos:
                    if cn.v_id is selected_video.v_id and cn.layer is 25:
                        videosBase[random_video - len(videosBase)].frequency += 1
                        cn.frequency = videosBase[random_video - len(videosBase)].frequency
                        cache_videos = sorted(cache_videos, key=attrgetter('frequency'))

                    elif cn.v_id is selected_video.v_id and cn.layer is 5:
                        videosEnhancement[random_video - len(videosBase)].frequency += 1
                        cn.frequency = videosEnhancement[random_video - len(videosBase)].frequency
                        cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                replacedBase = False
                replacedEnchancement = False
                i = 0
                while (not (replacedBase and replacedEnchancement)) and i < len(cache_videos):
                    if cache_videos[i].layer is 25 and (not replacedBase):
                        cache_videos[i] = videosBase[random_video - len(videosBase)]
                        replacedBase = True
                        cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                    elif cache_videos[i].layer is 5 and not replacedEnchancement:
                        cache_videos[i] = videosEnhancement[random_video - len(videosBase)]
                        replacedEnchancement = True
                        cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                    i += 1
            for i in cache_videos:
                print(i)

        elif question is 3:
            cache_videos = []
            if where_base == 0:
                for con in ordered_machines[0].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
            else:
                for con in ordered_machines[0].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                i = 0
                while ordered_machines[0].cache_size > 970 and i < len(cache_videos):
                    if cache_videos[i].layer is 5:
                        cache_videos.remove(cache_videos[i])
                        ordered_machines[0].cache_size -= 5
                    i += 1

                if ordered_machines[0].cache_size > 970:
                    cache_videos.remove(cache_videos[0])
                    ordered_machines[0].cache_size -= 25
                cache_videos.append(videosBase[random_video - len(videosBase)])
                cache_videos.append(videosEnhancement[random_video - len(videosBase)])
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))

            for i in cache_videos:
                print(i)

    elif (selected_video.layer is 25) and videoBase_founded:  # if SQ video founded
        print(f"Base Layer in {where_base}")
        videoBase_sent = False
        for x in range(len(channels)):
            if channels[x].c_id is ordered_machines[where_base].channel and not videoBase_sent:  # get Base layer
                if channels[x].availability is 1:  # if channel is available
                    h = channel.History()
                    h.v_id = selected_video.v_id
                    h.layer = 25
                    channels_history[x].history_queue.put(h)
                    channels[x].availability = 0
                    videoBase_sent = True
                else:  # if channel  is not available
                    for nx in range(len(channels)):
                        if channels[nx].availability is 1 and not videoBase_sent:
                            channels[x].availability = 1
                            channels[nx].availability = 0
                            h = channel.History()
                            h.v_id = selected_video.v_id
                            h.layer = 25
                            channels_history[x].history_queue.put(h)
                            videoBase_sent = True

        if question is 1:
            cache_videos = []
            for con in ordered_machines[0].contents:
                for vid in videosBase:
                    if con.v_id is vid.v_id and con.layer_id is 0:
                        cache_videos.append(vid)
                        break
                for vid in videosEnhancement:
                    if con.v_id is vid.v_id and con.layer_id is 1:
                        cache_videos.append(vid)
                        break
            tempBase_video = videosBase[random_video - len(videosBase)]
            temp_video = videosBase[random_video - len(videosBase)]
            firstBase_match = False
            for x in range(len(cache_videos)):
                if not firstBase_match:
                    if cache_videos[x].layer is 25:
                        temp_video = cache_videos[x]
                        cache_videos[x] = tempBase_video
                        tempBase_video = temp_video
                        continue
                if cache_videos[x].v_id is videosBase[random_video - len(videosBase)].v_id:
                    cache_videos[x] = tempBase_video

                temp_video = cache_videos[x]
                cache_videos[x] = videosBase
                tempBase_video = temp_video
            for i in cache_videos:
                print(i)

        elif question is 2:
            cache_videos = []
            if where_base == 0:
                for con in ordered_machines[where_base].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
            else:
                for con in ordered_machines[where_base].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                for cn in cache_videos:
                    if cn.v_id is selected_video.v_id and cn.layer is 25:
                        selected_video.frequency += 1
                        cn.frequency = selected_video.frequency
                        cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                        break
                replacedBase = False
                i = 0
                while not replacedBase and i < len(cache_videos):
                    if cache_videos[i].layer is 25:
                        cache_videos[i] = selected_video
                        cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                    i += 1
            for i in cache_videos:
                print(i)

        elif question is 3:
            cache_videos = []
            if where_base == 0:
                for con in ordered_machines[0].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))

            else:
                for con in ordered_machines[0].contents:
                    for vid in videosBase:
                        if con.v_id is vid.v_id and con.layer_id is 0:
                            vid.frequency += 1
                            cache_videos.append(vid)
                            break
                    for vid in videosEnhancement:
                        if con.v_id is vid.v_id and con.layer_id is 1:
                            cache_videos.append(vid)
                            break
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))
                i = 0
                while ordered_machines[0].cache_size > 975 and i < len(cache_videos):
                    if cache_videos[i].layer is 5:
                        cache_videos.remove(cache_videos[i])
                        ordered_machines[0].cache_size -= 5
                    i += 1

                if ordered_machines[0].cache_size > 975:
                    cache_videos.remove(cache_videos[0])
                    ordered_machines[0].cache_size -= 25
                cache_videos.append(videosBase[random_video - len(videosBase)])
                cache_videos = sorted(cache_videos, key=attrgetter('frequency'))

            for i in cache_videos:
                print(i)

total_videos = []
total_videos.append(ordered_machines[0].contents[0])
video_include = False
for x in ordered_machines:
    for y in x.contents:
        video_include = False
        for z in total_videos:
            try:
                if z.v_id is y.v_id and z.layer_id is y.layer_id:
                    video_include = True
                    break
            except:
                if z.v_id is y.v_id and z.layer_id is (0 if y.layer_id is 25 else 1):
                    video_include = True
                    break
        if not video_include:
            total_videos.append(y)
print(len(total_videos))
print("--- %s seconds ---" % (time.time() - start_time))
