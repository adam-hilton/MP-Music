def scale_value(value, min_in, max_in, min_out, max_out):
    scaled_value = min_out + (value - min_in)/(max_in - min_in)*(max_out - min_out)
    return int(scaled_value)