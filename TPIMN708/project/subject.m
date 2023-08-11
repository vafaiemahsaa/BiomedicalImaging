
classdef subject
    % saves the original cordinates of nodes for each subject, either that
    % is heallthy or patient

    properties
        sID;
        nodes;
        xyzcordiantes;
        crGraph;
        label;


    end
    methods
        function obj=subject(xsID)
            obj.sID=xsID;


        end
        function obj=SaveNodeCordinates(obj,xdim1,xdim2,xdim3,xID)
            temp_node =node(xdim1,xdim2,xdim3,xID);
            obj.nodes=[obj.nodes,temp_node];
        end
        function obj=ReturnCordinates(obj)
            obj.xyzcordiantes=[];
            [x,y]=size(obj.nodes);
            for i=1:y
                obj.xyzcordiantes=[obj.xyzcordiantes;[obj.nodes(i).dim1,obj.nodes(i).dim2,obj.nodes(i).dim3]];
            end
        end
        function obj=CreateGraph(obj,path_bold,mymask)
            mysub=load_nii(path_bold);

            [dim1,dim2,dim3,volume_fmri_data]=size(mysub.img);
            mynodes=zeros(1,570);
            count=1;
            for i=1:dim1
                for j=1:dim2
                    for k=1:dim3
                        isitnan=false;
                        isnode=true;
                        temp=(mymask(i,j,k));
                        if(temp<0.29)
                            isnode=false;
                            mymask(i,j,k)=0;
                        else

                            mymask(i,j,k)=1;
                        end
                        if isnode==true

                            temp=mysub.img(i,j,k,6:575).*mymask(i,j,k);
                            temp_nan=isnan(temp);
                            for x=1:size(temp_nan,2)
                                if temp_nan(x)
                                    isitnan=true;
                                end
                            end
                            if isitnan==false
                                mynodes(count,:)=temp;
                                obj=obj.SaveNodeCordinates(i,j,k,count);
                                count=count+1;
                            end


                        end

                    end
                end
            end
            [x,y]=size(mynodes);
            obj.crGraph=zeros(x,x);
            P_val=zeros(x,x);
            for i=1:x
                for j=1:x
                    [M,P]=corrcoef(mynodes(i,:),mynodes(j,:));

                    obj.crGraph(i,j)=M(1,2);
                    P_val(i,j)=P(1,2);
                end
            end
        end



    end
end