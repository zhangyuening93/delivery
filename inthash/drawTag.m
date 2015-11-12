% Number to generate
%num = [41, 10, 11, 12];
num = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
for k = 1:length(num)
    % Size of each block
    Size = 20;
    % Lower left corner of each box
    x = 0:Size:8*Size;
    y = 0:Size:8*Size;
    [x,y] = meshgrid(x,y);
    % Checkerboard values
    if mod(size(x,1),2)
        val = ones(size(x));
        val(:,1) = 1;
        val(:,8) = 1;
        val(1,:) = 1;
        val(8,:) = 1;
        % Setting error checking
        val(2,3) = 2;
        val(2,6) = 2;
        val(7,2) = 2;
        val(7,3) = 2;
        val(7,4) = 2;
        val(7,7) = 2;
        %%%%%%%%%%%%%%%%%%%%%%%%% Process %%%%%%%%%%%%%%%%%%%%%%%%%
        %val(1:2:end) = 2;
        for iter=1:6
            if bitand((bitshift(num(k),iter-6)),1) == 1
                val(3,8-iter) = 2;
            end
        end
        %%%%%%%%%%%%%%%%%%%%%%%%% Process %%%%%%%%%%%%%%%%%%%%%%%%%
    else
        val = ones(size(x,1)+1,size(x,2));
        val(1:2:end) = 2;
        val = val(1:end-1,:);
    end
    %val = val(1:8,1:8);
    % Coordinates of a box, relative to lower left corner
    xref = [0 0 Size Size 0];
    yref = [0 Size Size 0 0];
    % Add to get coordinates of each box
    xbox = bsxfun(@plus, x(:), xref);
    ybox = bsxfun(@plus, y(:), yref);
    % Plot using patch with RGB cdata
    cmap = [0 0 0; 1 1 1];
    val_2 = flip(val(1:8, 1:8));
    val(1:8,1:8) = val_2;
    col = permute(cmap(val(:), :), [3 1 2]);
    h = patch(xbox', ybox', col);
    h.LineStyle = 'none';
    h.EdgeColor = 'none';
    axis equal
    axis([0 8*Size 0 8*Size])
    set(gca, 'XTickLabel', '', 'YTickLabel', '', 'Visible', 'off')
    name = strcat('tag_',int2str(k));
    print(name,'-djpeg');
end
