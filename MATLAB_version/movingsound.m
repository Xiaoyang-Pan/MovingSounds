%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                           %
%            Playing moving Sound in headphones             %
%                                                           %
%      1.Imported a mp3 audio file                          %    
%      2.Controlled the magnitude of input audio signal     %
%      3.Added a time dealy to the input audio signal       %
%      4.Played the file with moving sound effects          %
%                                                           %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

%reading audio file in the same folder
[a, fs] = audioread('typewriter.mp3');

%If an input audio file only has one sound channel
%duplicate the sound channel
if size(a,2) == 1
    a = repmat(a,1,2);
end

%obtain a user input ranged from 1 to 2
%1 means slowest sound moving speed, 2 means fastest sound moving speed.prompt = ('Enter a positive number from 1 to 2: ');
prompt = "Please enter a number between 1 to 2; it relates to the speed of moving sounds: ";
factor = str2num(input(prompt,'s'));
goon = 1;

while goon == 1

    if isempty(factor)
       
        factor = str2num(input("Sorry, your input is invalid. Please enter a number between 1 to 2: ",'s'));
    
    else
        
        if factor < 1 || factor > 2
            factor = str2num(input("Sorry, your input is invalid. Please enter a number between 1 to 2: ",'s'));
        else
            goon = 0;       
        end
        
    end
    
end


%Controlled the magnitude of the audio signal respect to its total number 
%of audio samples 
audio_sample = size(a,1);
da = 1/audio_sample;

%choose the time offset to be 0.001% of the number of audio samples read
offset = round(1*10^(-5)*(audio_sample));

%Create a coefficient matrix to controll the magintude of the audio samples
%The sounds start from left moving to right in the beginning, and moving back to the right in the end
for c = 1:(audio_sample+offset)
   
     if c <= offset
        left_coe(:,c) = 1-c*da*factor;
        right_coe(:,c) = 0;
     
     elseif c <= audio_sample/2
        left_coe(:,c) = 1-c*da*factor;
        right_coe(:,c) = (c-offset)*da*factor;
     
     elseif c <= audio_sample/2 + offset
        left_coe(:,c) = 1-audio_sample/2*da*factor;
        right_coe(:,c) = (c-offset)*da*factor;
      
     elseif c <= audio_sample/2 + 2*offset
        left_coe(:,c) = 1-audio_sample/2*da*factor;
        right_coe(:,c) = audio_sample/2*da*factor;
         
     else    
        left_coe(:,c) = 1-audio_sample/2*da*factor + (c-audio_sample/2-2*offset)*da*factor;
        right_coe(:,c) = audio_sample/2*da*factor - (c-audio_sample/2-2*offset)*da*factor;
        
     end
     
 end
 
 %add the time offset to the coefficient
 newL = [zeros(1,offset) (a(:,1))'];
 newR = [(a(:,2))' zeros(1,offset)];
 
 %Obtain and play the moving sound effects
 V = [left_coe.*newL; right_coe.*newR]';
 sound(V,fs);
 
 clear V fs