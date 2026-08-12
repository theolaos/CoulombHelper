import moderngl
import moderngl_window as mglw
import numpy as np

class GraphApp(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "GPU Graphing Calculator"
    window_size = (800, 600)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Shader programs
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_vert;
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                out vec4 fragColor;
                uniform vec2 u_resolution;
                uniform vec2 u_offset;
                uniform float u_zoom;

                // Define the math function to plot: y = f(x)
                float f(float x) {
                    return sin(x);
                }

                void main() {
                    // Convert pixel coordinates to world space coordinates
                    vec2 st = (gl_FragCoord.xy - u_resolution * 0.5) / u_zoom + u_offset;
                    
                    // Evaluate function
                    float y = f(st.x);
                    
                    // Compute distance from current pixel's Y to the function's Y
                    float dist = abs(st.y - y);
                    
                    // Line thickness scaled by pixel size for sharp rendering
                    float line_thickness = 2.0 / u_zoom;
                    float alpha = smoothstep(line_thickness, 0.0, dist);

                    // Grid lines (X and Y axes)
                    vec3 color = vec3(0.08); // Background dark gray
                    if (abs(st.x) < line_thickness) color = vec3(0.4); // Y axis
                    if (abs(st.y) < line_thickness) color = vec3(0.4); // X axis

                    // Plot function curve in bright cyan
                    color = mix(color, vec3(0.0, 0.8, 1.0), alpha);

                    fragColor = vec4(color, 1.0);
                }
            '''
        )

        # Full-screen quad geometry
        vertices = np.array([
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
             1.0,  1.0,
        ], dtype='f4')

        vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.prog, vbo, 'in_vert')

        # Camera state
        self.offset = [0.0, 0.0]
        self.zoom = 100.0  # Pixels per unit

    def on_render(self, time: float, frametime: float):
        self.ctx.clear(0.0, 0.0, 0.0)
        
        # Pass uniforms to shader
        self.prog['u_resolution'].value = self.window_size
        self.prog['u_offset'].value = tuple(self.offset)
        self.prog['u_zoom'].value = self.zoom
        
        self.vao.render(moderngl.TRIANGLE_STRIP)

    def on_mouse_drag(self, x, y, dx, dy):
        # Pan the graph on left-click drag
        self.offset[0] -= dx / self.zoom
        self.offset[1] += dy / self.zoom

    def on_mouse_scroll_event(self, x_offset: float, y_offset: float):
        # Zoom in and out with scroll wheel
        if y_offset > 0:
            self.zoom *= 1.1
        elif y_offset < 0:
            self.zoom /= 1.1

if __name__ == '__main__':
    mglw.run_window_config(GraphApp)