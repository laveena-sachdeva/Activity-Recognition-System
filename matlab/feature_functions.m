classdef feature_functions
    methods(Static)
        
        function fftFeatureValues = fftFeatures(input,L)
            Y = fft(input);
            P2 = abs(Y/L);
            P1 = P2(1:uint8(L/2+1));
            P1(2:end-1) = 2*P1(2:end-1);
            [Data,I] = sort(abs(P1),'descend');
            % Returns only the top 3 peak values
            fftFeatureValues = P1(I(1:3,:));
            end

            % function which performs PSD and returns the top 3 peak values.
            function psdFeatureValues = psdFeatures(input)
            [pxx,w] = periodogram(input);
            psd = 10*log10(pxx);
            [Data,I] = sort(abs(psd),'descend');
            % Returns only the top 3 peak values
            psdFeatureValues = psd(I(1:3,:));
            end

            % function which performs DWT and returns the top 3 peak values.
            function dwtFeatureValues = dwtFeatures(input)
            [cA,cD] = dwt(input,'sym4');
            xrec = idwt(cA,zeros(size(cA)),'sym4');
            [Data,I] = sort(abs(xrec),'descend');
            % Returns only the top 3 peak values
            dwtFeatureValues = xrec(I(1:3,:));
            end
    end
end
