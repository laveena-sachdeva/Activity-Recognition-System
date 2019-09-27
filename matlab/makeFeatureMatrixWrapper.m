clc
root_path = "C:\Users\lavee\Documents\Semester_1\Data Mining\Assignment2\MyoData";
dirs = dir(root_path);
dir_inside = dirs(3).name;
pattern = ["eating", "noneating"];
pattern_eat = 'eating';
pattern_noneat = 'noneating';
for i=3:length(dirs)
    disp("inside_loop");
    disp(dirs(i).name);
    fork_path = root_path +"\"+ dirs(i).name +"\fork";
    dir_inside2 = dir(fork_path);
    "going inside";
    features_eat=[];
    features_noneat = [];
    file_out_eat = fork_path+"\featurematrix_eat_"+dirs(i).name+".csv";
    file_out_noneat = fork_path+"\featurematrix_noneat_"+dirs(i).name+".csv";
    for j=3:length(dir_inside2)
        if startsWith(dir_inside2(j).name,pattern_eat,'IgnoreCase', true)
            file_name = fork_path+"\"+dir_inside2(j).name;
            disp(file_name);
            feature_row = makeFeatureMatrix.make_feature_matrix(file_name,"IMU");
            features_eat = [features_eat; feature_row];
        end
        
        if startsWith(dir_inside2(j).name,pattern_noneat,'IgnoreCase', true)
            file_name = fork_path+"\"+dir_inside2(j).name;
            disp(file_name);
            feature_row = makeFeatureMatrix.make_feature_matrix(file_name,"IMU");
            features_noneat = [features_noneat; feature_row];
        end
        
    csvwrite(file_out_eat, features_eat)
    csvwrite(file_out_noneat, features_noneat)
        
    end
    
    
end

