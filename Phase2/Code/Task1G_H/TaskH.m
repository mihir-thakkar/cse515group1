function sim = TaskH(videoName1, videoName2)
histSimWeight = 0.4609;
siftSimWeight = 0.5157;
motionSimWeight = 0.0233;
histSim = TaskA(videoName1, videoName2);
siftSim = task1d(videoName1, videoName2);   
motionSim = task1e(videoName1, videoName2);
sim = histSim * histSimWeight + siftSim * siftSimWeight + motionSim * motionSimWeight;
end